import express from 'express';
import cors from 'cors';

const app = express();
const PORT = process.env.PORT || 3000;

// Enable CORS for frontend
app.use(cors());

// Example route
app.get('/', (req, res) => {
  res.send('Hello, World!');
});

// API route that returns JSON data
app.get('/api/data', (req, res) => {
  res.json({ message: 'This is some data from the backend' });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
