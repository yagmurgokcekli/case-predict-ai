from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import load_dataset

#verileri çek
train_data = load_dataset('json', data_files={'train': 'train_data.jsonl'}, split='train')
test_data = load_dataset('json', data_files={'test': 'test_data.jsonl'}, split='test')

#model ve tokenizer'ı yükle
model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

#tokenize
def tokenize_function(examples):
    return tokenizer(examples['input'], truncation=True, padding='max_length', max_length=512)

train_data = train_data.map(tokenize_function, batched=True)
test_data = test_data.map(tokenize_function, batched=True)

#TrainingArguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    logging_dir='./logs',
    logging_steps=10,
    save_steps=10_000,
    evaluation_strategy="steps",
    eval_steps=500,
    save_total_limit=2,
    warmup_steps=500,
    weight_decay=0.01,
    logging_first_step=True,
)

#eğitimi başlat
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    eval_dataset=test_data,
)

#modeli eğit
trainer.train()

#modeli kaydet
model.save_pretrained('./gpt2_karar_metni')
tokenizer.save_pretrained('./gpt2_karar_metni')



