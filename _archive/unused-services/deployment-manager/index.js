const express = require('express');
const Docker = require('dockerode');
const YAML = require('yaml');

const app = express();
const PORT = process.env.PORT || 8083;
const docker = new Docker();

app.use(express.json());

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'deployment-manager' });
});

// Deploy application
app.post('/deploy', async (req, res) => {
  try {
    const { name, image, config = {} } = req.body;
    
    const containerConfig = {
      Image: image,
      name: `adep-${name}`,
      Env: config.env || [],
      ExposedPorts: config.ports ? config.ports.reduce((acc, port) => {
        acc[`${port}/tcp`] = {};
        return acc;
      }, {}) : {},
      HostConfig: {
        PortBindings: config.ports ? config.ports.reduce((acc, port) => {
          acc[`${port}/tcp`] = [{ HostPort: port.toString() }];
          return acc;
        }, {}) : {}
      }
    };

    // Create and start container
    const container = await docker.createContainer(containerConfig);
    await container.start();

    const deploymentId = container.id;
    
    res.json({
      deploymentId,
      status: 'deployed',
      name,
      image,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Deployment error:', error);
    res.status(500).json({ error: 'Failed to deploy application' });
  }
});

// Get deployment status
app.get('/deploy/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const container = docker.getContainer(id);
    const info = await container.inspect();
    
    res.json({
      deploymentId: id,
      status: info.State.Running ? 'running' : 'stopped',
      created: info.Created,
      image: info.Config.Image,
      ports: info.NetworkSettings.Ports
    });
  } catch (error) {
    console.error('Status check error:', error);
    res.status(404).json({ error: 'Deployment not found' });
  }
});

// Stop deployment
app.delete('/deploy/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const container = docker.getContainer(id);
    
    await container.stop();
    await container.remove();
    
    res.json({
      deploymentId: id,
      status: 'stopped',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Stop deployment error:', error);
    res.status(500).json({ error: 'Failed to stop deployment' });
  }
});

// List deployments
app.get('/deployments', async (req, res) => {
  try {
    const containers = await docker.listContainers({ all: true });
    const deployments = containers
      .filter(container => container.Names.some(name => name.startsWith('/adep-')))
      .map(container => ({
        deploymentId: container.Id,
        name: container.Names[0].replace('/adep-', ''),
        image: container.Image,
        status: container.State,
        created: container.Created,
        ports: container.Ports
      }));
    
    res.json({ deployments });
  } catch (error) {
    console.error('List deployments error:', error);
    res.status(500).json({ error: 'Failed to list deployments' });
  }
});

// Scale deployment
app.post('/deploy/:id/scale', async (req, res) => {
  try {
    const { id } = req.params;
    const { replicas } = req.body;
    
    // For Docker, we'll simulate scaling by creating additional containers
    // In a real implementation, this would use Docker Swarm or Kubernetes
    
    res.json({
      deploymentId: id,
      replicas,
      status: 'scaled',
      timestamp: new Date().toISOString(),
      message: 'Scaling simulation - would implement with orchestrator'
    });
  } catch (error) {
    console.error('Scale deployment error:', error);
    res.status(500).json({ error: 'Failed to scale deployment' });
  }
});

// Rollback deployment
app.post('/deploy/:id/rollback', async (req, res) => {
  try {
    const { id } = req.params;
    const { version } = req.body;
    
    res.json({
      deploymentId: id,
      version,
      status: 'rolled_back',
      timestamp: new Date().toISOString(),
      message: 'Rollback simulation - would implement version control'
    });
  } catch (error) {
    console.error('Rollback deployment error:', error);
    res.status(500).json({ error: 'Failed to rollback deployment' });
  }
});

app.listen(PORT, () => {
  console.log(`Deployment Manager running on port ${PORT}`);
});

module.exports = app;