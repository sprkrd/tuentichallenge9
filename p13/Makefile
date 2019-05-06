all: sampleOutput testOutput submitOutput

sampleOutput: sampleInput main.py
	./main.py < sampleInput > sampleOutput
	cat sampleOutput

testOutput: testInput main.py
	./main.py < testInput > testOutput

submitOutput: submitInput main.py
	./main.py < submitInput > submitOutput

clean:
	rm -rf *Output

