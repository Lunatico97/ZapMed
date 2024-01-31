# ZapMed (t5-small-MedicoSummarizer)

This model was fine-tuned on t5-small on 25,000 PubMed articles for 10 epochs.
It achieves the following results on the evaluation set:

### Training hyperparameters

The following hyperparameters were used during training:
- batch_size = 16
- training_precision: float32
- epochs = 10
- learning_rate = 2e-5

### Training results

|epoch|eval_loss         |eval_rouge1|eval_rouge2|eval_rougeL|eval_rougeLsum|eval_gen_len|
|-----|------------------|-----------|-----------|-----------|--------------|------------|
|1.0  |3.0605552196502686|0.302      |0.0693     |0.1841     |0.1842        |116.916     |
|2.0  |3.0079214572906494|0.3192     |0.0749     |0.1943     |0.1944        |122.076     |
|3.0  |2.9787817001342773|0.3209     |0.0758     |0.1957     |0.1958        |122.95      |
|4.0  |2.95868182182312  |0.3226     |0.0772     |0.1978     |0.1978        |123.593     |
|5.0  |2.943807601928711 |0.3186     |0.0743     |0.1959     |0.1959        |123.822     |
|6.0  |2.9342598915100098|0.3194     |0.0755     |0.1962     |0.1961        |123.834     |
|7.0  |2.927173376083374 |0.3205     |0.0758     |0.1967     |0.1968        |123.967     |
|8.0  |2.9225199222564697|0.3211     |0.0763     |0.1974     |0.1975        |124.178     |
|9.0  |2.9196181297302246|0.32       |0.0762     |0.1964     |0.1964        |124.136     |
|10.0 |2.9186391830444336|0.3209     |0.0766     |0.1965     |0.1965        |124.115     |

## Test Metrics
{'test_loss': 2.8919856548309326,
 'test_rouge1': 0.3207,
 'test_rouge2': 0.0741,
 'test_rougeL': 0.1955,
 'test_rougeLsum': 0.1955,
 'test_gen_len': 124.285,
 'test_runtime': 335.298,
 'test_samples_per_second': 5.965,
 'test_steps_per_second': 0.373}


### Framework versions

- Transformers 4.35.2
- TensorFlow 2.15.0
- Datasets 2.16.1
- Tokenizers 0.15.0
