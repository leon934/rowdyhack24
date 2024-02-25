import React from 'react';

type wordListTypeProps = {
	wordList: string[];
};

const WordListComponent: React.FC<wordListTypeProps> = ({ wordList }) => {
	return (
		<ul>
			{wordList.map((word) => (
				<li key={word}>{word}</li>
			))}
		</ul>
	);
};

export default WordListComponent;
