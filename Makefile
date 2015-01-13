dir:
	python inegi_explore.py dir geodesia.inegi.org.mx "/home/rgna" rgnaftp rgnaftp > inegi.json
	python prune.py inegi.json > inegi-temp.json
	mv inegi-temp.json inegi.json