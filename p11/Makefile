CXX_FLAGS=-Wall -Wextra -pedantic -O3

main: main.cpp
	g++ $(CXX_FLAGS) main.cpp -o main

tests: sampleOutput testOutput submitOutput

sampleOutput: sampleInput main
	./main < sampleInput > sampleOutput
	cat sampleOutput

testOutput: testInput main
	./main < testInput > testOutput

submitOutput: submitInput main
	./main < submitInput > submitOutput

clean:
	rm -rf main *Output

