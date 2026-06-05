# Storage Tiering - Gravitational Optimization

## Purpose
Automatically tier storage based on access patterns using gravitational search.

## Tiers

1. **Local NVMe**: Hot data (frequent access) - "Heavy Mass"
2. **Network SSD**: Warm data (occasional access)
3. **Object Storage**: Cold data (rare access)
4. **Glacier**: Archive (almost never accessed) - "Light Mass"

Gravitational algorithm pulls frequently accessed data toward local storage.
