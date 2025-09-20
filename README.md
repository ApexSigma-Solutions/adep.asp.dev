# ADEP - Autonomous DevEx Pipeline

Autonomous DevEx Pipeline : ApexSigma EcoSystem of agentic development services within a self contained docker composed network.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/ApexSigma-Solutions/adep.asp.dev.git
cd adep.asp.dev

# Start the pipeline
./scripts/start.sh
```

## 🏗️ Architecture

ADEP consists of 5 core microservices orchestrated through Docker Compose:

- **API Gateway** (8080) - Request routing and rate limiting
- **Pipeline Orchestrator** (8081) - Development pipeline management
- **Code Analyzer** (8082) - Static code analysis and quality metrics
- **Deployment Manager** (8083) - Container deployment and scaling
- **Agent Coordinator** (8084) - Autonomous agent coordination

## 🛠️ Services

### Core Services
- **Redis** - Caching and message queuing
- **PostgreSQL** - Persistent data storage
- **Prometheus** - Metrics collection
- **Grafana** - Monitoring dashboards

## 📚 Documentation

Detailed documentation is available in the [docs](./docs/) directory.

## 🔧 Development

Each service can be developed independently:

```bash
cd services/[service-name]
npm install
npm run dev
```

## 📊 Monitoring

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.
