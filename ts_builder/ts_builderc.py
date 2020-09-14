class TS_Builder:
	
	def __init__(self, ppdb_path = "./l-lexical"):
		#self.output_prefix_ = "./"
		self.output_prefix_ = "./output/"
		
		self.sql_statements_ = self.output_prefix_ + "generated_sql_statements.txt"
		self.nl_statements_ = self.output_prefix_ + "generated_nl_statements"
		self.paraphrased_ = self.output_prefix_ = "paraphrased_nl_statements.txt"
		
		self.sqlaggr_ = self.output_prefix_ + "manual_sqlaggr_statements.txt"
		self.nlaggr_ = self.output_prefix_ + "manual_nlaggr_statements.txt"
		self.paraphrasedaggr_ = self.output_prefix_ + "paraphrased_nlaggr_statements.txt"
		
		self.ts_ = self.output_prefix_ + "training_set"
		
		self.ppdb_path_ = ppdb_path
		
	def create_sql_nl(self):
		
		tablename = "patients"
		sql_fields = ["id", "first_name", "last_name", "diagnosis", "gender", "length_of_stay", "age"]
		nl_fields = {"id" :"ids", "first_name" : "name", "last_name": "surname", "diagnosis" : "disease", "gender" : "gender", "length_of_stay" : "hospilization period", "age" : "age"}
		annot = {"id" : "@ID", "first_name" : "@FIRST_NAME", "last_name" : "@LAST_NAME", "diagnosis" : "@DIAGNOSIS", "gender" : "@GENDER", "length_of_stay" : "@LENGTH_OF_STAY", "age" : "@AGE"}
		
		sql_from = "SELECT sclause FROM table"
		sql_where = "SELECT sclause FROM table WHERE wclause"
		nlang_1 = "what are the fields of all patients?"
		nlang_2 = "show the fields of all patients?"
		
		sql_from_instant = sql_from.replace("table", tablename)
		sql_where_instant = sql_where.replace("table", tablename)
		
		# calculate the powerset of the sql fields
		pset = self.powerset(sql_fields)
		from_queries = []
		where_queries_intermediate = []
		nlang_queries = []
		
		pset = list(pset)
		pset_size_two = [x for x in pset if len(x) <= 2]
		
		for subset in pset:
			if len(subset) == 0:
				continue
			elif len(subset) == len(sql_fields):
				sclause = "*"
				nl_clause = "info"
			else:
				tempset = list(subset)
				if "id" not in subset:
					tempset = ["id"] + tempset
				sclause = ",".join(tempset) # ad-hoc solution for angular: include the id in all SELECT clauses
				nl_clause = ",".join(nl_fields[x] for x in subset)
			from_queries.append(sql_from_instant.replace("sclause", sclause))
			where_queries_intermediate.append(sql_where_instant.replace("sclause", sclause))
			nlang_queries.append(nlang_1.replace("fields", nl_clause))
			nlang_queries.append(nlang_2.replace("fields", nl_clause))
			
		where_queries = []
		i = -2
		
		for temp_query in where_queries_intermediate:
			i = i + 2
			nlang_query_1 = nlang_queries[i]
			nlang_query_2 = nlang_queries[i+1]
			for subset in pset_size_two:
				if len(subset) == 0:
					continue
				else:
					wclause = " AND ".join(x + " = " + annot[x] for x in subset)
					nl_clause = ",".join(nl_fields[x] + " " + annot[x] for x in subset)
					nl_clause = " with " + nl_clause + "?"
				where_queries.append(temp_query.replace("wclause", wclause))
				nlang_queries.append(nlang_query_1.replace("?", nl_clause))
				nlang_queries.append(nlang_query_2.replace("?", nl_clause))
		
		all_queries = from_queries + where_queries

		f = open(self.sql_statements_, "w")
		for q in all_queries:
			f.write(q + "\n")
		f.close()


		f = open(self.nl_statements_, "w")
		for q in nlang_queries:
			f.write(q + "\n")
		f.close()

	def lemmatize(self, lemmatizer, sentence, stop_words):
		
		import nltk
		from nltk.tokenize import word_tokenize
		#from nltk.stem.porter import PorterStemmer
		
		lemmatized_word_list = []
		prev = ""
		
		for word in nltk.word_tokenize(sentence):
			if word in stop_words:
				lemmatized_word_list.append(word)
			else:
				if prev == "@":
					lemmatized_word_list.append(word)
				else:
					lemmatized_word_list.append(lemmatizer.stem(word))
			prev = word
			
		retVal = lemmatized_word_list[0]
		prev = retVal
		for word in lemmatized_word_list[1:]:
			if prev != "@":
				retVal = retVal + " " + word
			else:
				retVal = retVal + word
			prev = word
		return retVal
		
	def powerset(self, iterable):
		from itertools import chain, combinations
		
		s = list(iterable)
		return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

	def paraphrase(self, sql_input, nl_input, file_output):
		
		import ppdb
		import nltk
		from nltk.corpus import stopwords
		from nltk.tokenize import word_tokenize
		from nltk.stem.porter import PorterStemmer
	
		# Load the nltk stopwords and enchance them with symbols that we will encounter
		stop_words = stopwords.words('english')
		extra_stop_words = ",.?<>@="
		for word in extra_stop_words:
			stop_words.append(word)
			
		lemmatizer = PorterStemmer()

		print("Loading ppdb file")
		ppdb_rules = ppdb.load_ppdb(self.ppdb_path_)
		print("Loaded ppdb file")

		# READ FROM FILES - Each sql statement corresponds to 2 nl statements
		sql_file = open(sql_input)
		nl_file = open(nl_input)

		sql_statements = sql_file.readlines()
		nl_statements = nl_file.readlines()

		sql_file.close()
		nl_file.close()

		sql_nl_matches = {} # holds {sql_key : [list of nl statements paraphrased]

		print("Dictionary building started")
		# Start building the dictionary
		for i in range(0, len(sql_statements)):
			j = 2*i # j: index to scan nl_statements list
			NL1 = nl_statements[j].replace("\n","")
			NL2 = nl_statements[j+1].replace("\n","")
			
				# break nl statement in words
			wordlist_1 = word_tokenize(NL1)
			wordlist_2 = word_tokenize(NL2)
			
			paraphrases = [self.lemmatize(lemmatizer, NL1, stop_words), self.lemmatize(lemmatizer, NL2, stop_words)] # a list of the nl_statements paraphrases

			# for every non-stop word, get its synonyms and replace each synonym by making a copy of the original nl_statement
			for word in wordlist_1:
				if word not in stop_words:
					synonyms = ppdb_rules.get_rhs(word)
					if len(synonyms) > 0:
						for synonym in synonyms:
							lemmatized_paraphrase = self.lemmatize(lemmatizer, NL1.replace(word, synonym[0]), stop_words)
							paraphrases.append(lemmatized_paraphrase)
							#paraphrases.append(NL1.replace(word, synonym[0])) # synonym is a single element tuple
							
			# repeat for the second nl_statement
			for word in wordlist_2:
				if word not in stop_words:
					synonyms = ppdb_rules.get_rhs(word)
					if len(synonyms) > 0:
						for synonym in synonyms:
							lemmatized_paraphrase = self.lemmatize(lemmatizer, NL2.replace(word, synonym[0]), stop_words)
							paraphrases.append(lemmatized_paraphrase)
							#paraphrases.append(NL2.replace(word, synonym[0])) # synonym is a single element tuple
			
			# add the key and the value in the dictionary
			sql_nl_matches[sql_statements[i]] = paraphrases
		print("Dictionary building finished")

		print("Writing results to file")
		filename =  file_output
		output_file = open(filename, "w")
		for key in sql_nl_matches.keys():
			for value in sql_nl_matches[key]:
				output_file.write(value + "\t" + key)
		output_file.close()
		
	def merge(self):
		f = open(self.paraphrased_, "r")
		f2 = open(self.paraphrasedaggr_, "r")
		merged = open(self.ts_, "w")
		
		content1 = f.readlines()
		content2 = f2.readlines()
		
		for i in content1:
			merged.write(i)
		
		for i in content2:
			merged.write(i)
		
		f.close()
		f2.close()
		merged.close()
		
	def build(self):
		self.create_sql_nl()
		self.paraphrase(self.sql_statements_, self.nl_statements_, self.paraphrased_)
		self.paraphrase(self.sqlaggr_, self.nlaggr_, self.paraphrasedaggr_)
                self.merge()
