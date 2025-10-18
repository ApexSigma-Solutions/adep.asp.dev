const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;

const app = express();
const PORT = process.env.PORT || 8082;

app.use(express.json());

// Configure multer for file uploads
const upload = multer({ dest: '/tmp/uploads/' });

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'code-analyzer' });
});

// Analyze code quality
app.post('/analyze', upload.array('files'), async (req, res) => {
  try {
    const { files } = req;
    const results = [];

    for (const file of files) {
      const content = await fs.readFile(file.path, 'utf8');
      const analysis = analyzeCode(content, file.originalname);
      results.push({
        filename: file.originalname,
        ...analysis
      });
    }

    // Cleanup uploaded files
    for (const file of files) {
      await fs.unlink(file.path);
    }

    res.json({
      timestamp: new Date().toISOString(),
      results,
      summary: generateSummary(results)
    });
  } catch (error) {
    console.error('Analysis error:', error);
    res.status(500).json({ error: 'Failed to analyze code' });
  }
});

// Code repository analysis
app.post('/analyze-repo', async (req, res) => {
  try {
    const { repoUrl, branch = 'main' } = req.body;
    
    // Simulate repository analysis
    const analysis = {
      repoUrl,
      branch,
      timestamp: new Date().toISOString(),
      metrics: {
        linesOfCode: Math.floor(Math.random() * 10000) + 1000,
        complexity: Math.floor(Math.random() * 100) + 1,
        maintainabilityIndex: Math.floor(Math.random() * 100) + 1,
        testCoverage: Math.floor(Math.random() * 100) + 1
      },
      issues: [
        {
          type: 'warning',
          message: 'Unused variable detected',
          file: 'src/index.js',
          line: 42
        },
        {
          type: 'error',
          message: 'Missing semicolon',
          file: 'src/utils.js',
          line: 15
        }
      ],
      recommendations: [
        'Consider adding more unit tests to improve coverage',
        'Refactor complex functions to improve maintainability',
        'Add JSDoc comments for better documentation'
      ]
    };

    res.json(analysis);
  } catch (error) {
    console.error('Repository analysis error:', error);
    res.status(500).json({ error: 'Failed to analyze repository' });
  }
});

function analyzeCode(content, filename) {
  const lines = content.split('\n');
  const analysis = {
    linesOfCode: lines.length,
    complexity: calculateComplexity(content),
    issues: findIssues(content),
    suggestions: generateSuggestions(content, filename)
  };

  return analysis;
}

function calculateComplexity(content) {
  // Simple complexity calculation based on control structures
  const patterns = [/if\s*\(/g, /for\s*\(/g, /while\s*\(/g, /switch\s*\(/g, /catch\s*\(/g];
  let complexity = 1; // Base complexity
  
  patterns.forEach(pattern => {
    const matches = content.match(pattern);
    if (matches) {
      complexity += matches.length;
    }
  });

  return complexity;
}

function findIssues(content) {
  const issues = [];
  
  // Check for common issues
  if (content.includes('console.log')) {
    issues.push({ type: 'warning', message: 'Console.log statements found' });
  }
  
  if (content.includes('eval(')) {
    issues.push({ type: 'error', message: 'Use of eval() is dangerous' });
  }
  
  if (content.includes('var ')) {
    issues.push({ type: 'info', message: 'Consider using let/const instead of var' });
  }

  return issues;
}

function generateSuggestions(content, filename) {
  const suggestions = [];
  
  if (filename.endsWith('.js') && !content.includes('use strict')) {
    suggestions.push('Add "use strict" directive');
  }
  
  if (content.length > 1000) {
    suggestions.push('Consider breaking this file into smaller modules');
  }
  
  return suggestions;
}

function generateSummary(results) {
  const totalFiles = results.length;
  const totalLines = results.reduce((sum, r) => sum + r.linesOfCode, 0);
  const totalIssues = results.reduce((sum, r) => sum + r.issues.length, 0);
  const avgComplexity = results.reduce((sum, r) => sum + r.complexity, 0) / totalFiles;

  return {
    totalFiles,
    totalLines,
    totalIssues,
    averageComplexity: Math.round(avgComplexity * 100) / 100
  };
}

app.listen(PORT, () => {
  console.log(`Code Analyzer running on port ${PORT}`);
});

module.exports = app;