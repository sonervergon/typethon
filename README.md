# Monorepo boilerplate

A pnpm monorepo with Turborepo containing a Python backend service and a Vite web application.

## Monorepo Structure

```
api-monorepo/
├── apps/                 # Application packages
│   ├── core/             # Core Python API service
│   │   └── bin/          # Core-specific scripts
│   └── web/              # Vite web application
├── packages/             # Shared packages (libraries, components, etc.)
├── package.json          # Root package configuration
├── pnpm-workspace.yaml   # Workspace configuration
└── turbo.json            # Turborepo configuration
```

## Getting Started

### Prerequisites

- Node.js 16+
- pnpm 8+
- Python 3.9+ (for Python services)

### Installation

1. Install dependencies:

```bash
pnpm install
```

2. Set up Python environments:

```bash
pnpm setup-env
```

This will run the setup scripts for all Python services in parallel using Turborepo.

### Development

Start all services in development mode:

```bash
pnpm dev
```

This will start all the services in parallel using Turborepo.

## Available Services

### Core API Service

The Core API service is a Python backend service using FastAPI with a layered architecture.

### Web Application

A modern Vite-powered web application that connects to the Core API.

## Monorepo Scripts

- `pnpm dev` - Run all services in development mode using Turborepo
- `pnpm setup-env` - Initialize Python environments for all services in parallel
- `pnpm build` - Build all packages using Turborepo
- `pnpm lint` - Lint all packages using Turborepo

## Adding New Services

1. Create a new directory in the appropriate folder:

   - For applications: `apps/<service-name>`
   - For shared packages: `packages/<package-name>`

2. Add the service to the workspace by updating its package.json

3. Add the service to the Turborepo pipeline in `turbo.json` if needed

4. The service will be automatically included in the root dev command

## Contributing

Please see [DEVELOPMENT.md](./apps/core/DEVELOPMENT.md) for contribution guidelines.
