Italian Sentiment is a Python package for sentiment analysis in Italian language.

This project draws inspiration from [Sentita](https://drive.google.com/file/d/1s1BW3T_BysAhVZPai-3AUXpb68aYjQTS/view?usp=sharing).


## Installation

You can install the package using `pip`:

```bash
cd path/to/italian_sentiment

pip install .
```

##Usage
```python
from italian_sentiment import SentimentAnalyzer

# Initialize the SentimentAnalyzer
analyzer = SentimentAnalyzer()

# Sentences to analyze
sentences_to_analyze = ["voglio andare a vivere in montagna", "voglio andare a vivere in montagna 💩"]

# Predict sentiment for each sentence
results = analyzer.predict_sentiment(sentences_to_analyze)

# Print the results
for result in results:
    print(result)
```
![Example](example.png)

##License

This project is licensed under the MIT License - see the LICENSE file for details.

For more information and detailed usage instructions, please refer to the documentation.
