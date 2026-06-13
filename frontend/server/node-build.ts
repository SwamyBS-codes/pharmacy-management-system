import express from 'express';
import path from 'path';

const app = express();

// Serve the client build (dist/spa)
const staticDir = path.resolve(__dirname, '../dist/spa');
app.use(express.static(staticDir));

app.get('*', (_req, res) => {
  res.sendFile(path.join(staticDir, 'index.html'));
});

export default app;
