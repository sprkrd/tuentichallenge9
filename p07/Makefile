Main.class: Main.java
	javac Main.java

tests: sampleOutput testOutput submitOutput

sampleOutput: sampleInput Main.class
	java Main < sampleInput > sampleOutput
	cat sampleOutput
	diff sampleOutput sampleOutput.given

testOutput: testInput Main.class
	java Main < testInput > testOutput

submitOutput: submitInput Main.class
	java Main < submitInput > submitOutput

clean:
	rm -rf Main.class *Output

