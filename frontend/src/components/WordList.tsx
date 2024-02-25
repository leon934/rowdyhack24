import React from 'react';
import wordsData from '../data/DummyWords.json';

const words: string[] = wordsData.words;

const WordList: React.FC = () => {
	return (
		<ul>
			{words.map((word) => (
				<li key={word}>{word}</li>
			))}
		</ul>
	);
};

export default WordList;
