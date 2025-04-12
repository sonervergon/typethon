# API Monorepo

A pnpm monorepo with Turborepo containing a Python backend service and related applications.

## Monorepo Structure

```
api-monorepo/
├── apps/                 # Application packages
│   └── core/             # Core Python API service
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
pnpm init-python
```

### Development

Start all services in development mode:

```bash
pnpm dev
```

This will start all the services in parallel using Turborepo.

## Available Services

### Core API Service

The Core API service is a Python backend service using FastAPI with a layered architecture.

- **Location**: `./apps/core`
- **Documentation**:
  - [Core API README](./apps/core/README.md)
  - [Development Guide](./apps/core/DEVELOPMENT.md)
- **Running**: Available through the root `pnpm dev` command or individually with `pnpm dev:core`
- **Testing**: `pnpm test:core`

## Monorepo Scripts

- `pnpm dev` - Run all services in development mode using Turborepo
- `pnpm init-python` - Initialize Python environments
- `pnpm dev:core` - Run the core API in development mode individually
- `pnpm test:core` - Run tests for the core API
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
