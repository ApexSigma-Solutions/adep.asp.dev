const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = process.env.PORT || 8080;

// Security middleware
app.use(helmet());
app.use(cors());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'api-gateway' });
});

// Proxy routes to microservices
app.use('/api/pipeline', createProxyMiddleware({
  target: 'http://pipeline-orchestrator:8081',
  changeOrigin: true,
  pathRewrite: { '^/api/pipeline': '' }
}));

app.use('/api/analyze', createProxyMiddleware({
  target: 'http://code-analyzer:8082',
  changeOrigin: true,
  pathRewrite: { '^/api/analyze': '' }
}));

app.use('/api/deploy', createProxyMiddleware({
  target: 'http://deployment-manager:8083',
  changeOrigin: true,
  pathRewrite: { '^/api/deploy': '' }
}));

app.use('/api/agents', createProxyMiddleware({
  target: 'http://agent-coordinator:8084',
  changeOrigin: true,
  pathRewrite: { '^/api/agents': '' }
}));

app.listen(PORT, () => {
  console.log(`API Gateway running on port ${PORT}`);
});

module.exports = app;