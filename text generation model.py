import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

# Read data from file and preprocess
with open('TinyStories-valid.txt', 'r') as file:
    data = file.read()
    words = data.split()
    vocab = set(words)
word_to_index = {word: index for index, word in enumerate(vocab)}
sequences = []
sequence_length = 30

for i in range(sequence_length, len(words)):
    sequence = words[i-sequence_length:i]
    target_word = words[i]
    sequences.append((sequence, target_word))

# Define the text generation model
class TextGenerationModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super(TextGenerationModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        lstm_out, _ = self.lstm(x)
        out = self.fc(lstm_out[:, -1, :])
        return out

# Initialize and train the model
model = TextGenerationModel(vocab_size=len(vocab), embedding_dim=100, hidden_dim=256)
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()

class TextDataset(Dataset):
    def __init__(self, sequences, word_to_index):
        self.sequences = sequences
        self.word_to_index = word_to_index

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        sequence, target_word = self.sequences[idx]
        sequence = torch.tensor([self.word_to_index[word] for word in sequence], dtype=torch.long)
        target = torch.tensor(self.word_to_index[target_word], dtype=torch.long)
        return sequence, target

dataset = TextDataset(sequences, word_to_index)
data_loader = DataLoader(dataset, batch_size=32, shuffle=True)
num_epochs = 10

for epoch in range(num_epochs):
    for batch in data_loader:
        sequence, target = batch
        outputs = model(sequence)
        loss = loss_fn(outputs, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

# Text generation function
def generate_text(seed_text, model, vocab, word_to_index, index_to_word, sequence_length, gen_length):
    model.eval()
    seed = torch.tensor([word_to_index[word] for word in seed_text.split()], dtype=torch.long).unsqueeze(0)
    generated_text = seed_text

    for _ in range(gen_length):
        with torch.no_grad():
            output = model(seed)

        _, next_word_index = torch.max(output, dim=1)
        next_word = index_to_word[next_word_index.item()]
        generated_text += " " + next_word

        seed = torch.cat((seed[:, -sequence_length+1:], next_word_index.unsqueeze(0)), dim=1)

    return generated_text

# Interactive text generation loop
while True:
    user_input = input("Enter a seed text (type 'exit' to stop): ")

    if user_input.lower() == 'exit':
        print("Exiting the interactive text generation.")
        break

    generated_text = generate_text(user_input, model, vocab, word_to_index, {index: word for word, index in word_to_index.items()}, sequence_length=30, gen_length=100)
    print("Generated Text:", generated_text)
