<h1>Google Sentence auto complete project</h1>
<h3>By Yinon Tzumi, Amit Ein-Dor, Orel Aviad</h3>

<h1>Description</h1>
<p>
A program that provides an auto complete for an input by the user.</p>
<p>
The sentence suggestions are selected out of a directory of multiple files,
that can be divided into sub directories.
</p>
<p>
The program present the 5 top suggestions, based on a score that calculate how 
similar the real sentence from the user's input.
</p>
<p>
The project was planned and mentored by Google employees.
</p>

<h1>The Algorithm</h1>
<h5>OFFLINE:</h5>
<p>First we extract all the sentences out of the directories and sub-directories, and save them with all the right data in the database</p>

<h5>ONLINE:</h5>
<p>First, when we get an input from the user we will strip it from unwanted signs such as ?!*</p>
<p>We split the input, and count how many input words isn't found in the text.</p>
<p>Incase there is only one misspelled word, we will divide the sentence into prefix and suffix, and check for the sentences that has both the prefix and the suffix (in the right order) using list intersection. </p>
<p>We take the word in the middle of each result sentence and compare it to the misspelled word in a function that tell us how and if we can correct the input to match it.</p>
<p>Based on the result we set the score and return 5 sentences with the best score.</p>

<h1>Data Structure used</h1>
<p>1. A Dictionary that holds as key every word that appears in the text, and the content is every sentence that contain this word.</p>
<p>2. A List of Sentences, each sentence is an object that holds the text of the sentence, the file it was taken from and the exact line in the file.</p>

<h1>Execution</h1>
<p>1. Please place the data archive in a folder named 'resources'
and run the main.py file using default configuration.
</p>