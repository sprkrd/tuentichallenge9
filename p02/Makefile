all: testOutput submitOutput

testOutput: testInput main.py
	./main.py < testInput > testOutput

submitOutput: submitInput main.py
	./main.py < submitInput > submitOutput

clean:
	rm -rf testOutput submitOutput

