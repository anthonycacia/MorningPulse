# MorningPulse

MorningPulse is a lightweight, containerized FastAPI service that delivers automated morning market briefings directly to Discord using webhooks; no Developer account or Discord App necessary.

Each morning, MorningPulse gathers foreign exchange market data, calculates daily changes and moving averages, formats a human-readable report, then delivers it to a Discord channel.  

Converted from a legacy project that was one long script. MorningPulse demonstrates:  

- FastAPI service development  
- Docker containerization  
- Environment-based configuration  
- External API integration  
- Discord webhook automation  
- Persistent storage with Docker volumes  
- GitHub Actions CI/CD workflows  

# Current Features

✅ Daily foreign exchange reports

✅ Historical moving averages

✅ Daily price change calculations

✅ Randomized morning greetings

✅ Discord webhook delivery

✅ Persistent cache volume

✅ Dockerized deployment

✅ GitHub Actions automation

# Architecture
FXMarketAPI  
     ↓
 FXProvider  
     ↓
 Market Transform  
     ↓
 Report Builder  
     ↓
 Discord Webhook  

# Example Report

MorningPulse currently reports:

- Euro (EURUSD)  
- British Pound (GBPUSD)  
- Canadian Dollar (CADUSD)  
- Australian Dollar (AUDUSD)  
- New Zealand Dollar (NZDUSD)  
- Japanese Yen (USDJPY)  

Each report includes:

- Current value  
- Direction from previous trading day  
- Daily percentage change  
- Short-term moving average  
- Long-term moving average  

# Requirements
Docker  
Docker Compose  
FXMarketAPI account and API key  
Discord webhook URL  

# Quick Start

Clone the repository:  

```
git clone <repo-url>
cd MorningPulse  

```
Create your environment file:  

```
cp .env.example .env
```

Edit .env:  

DISCORD_WEBHOOK=your_webhook_url  
FOREX_API_KEY=your_api_key  
FOREX_PAIRS=EURUSD,GBPUSD,CADUSD,AUDUSD,NZDUSD,USDJPY
MY_NAME=World # Insert your name

Build and start the service:  

```
docker compose up --build
```

# API Endpoints
### GET /health

Returns service health information.

### GET /debug/fx

Returns raw foreign exchange data.

### GET /msg

Builds a report without sending it to Discord.

### POST /run/morning-pulse

Builds and sends the report to Discord.

### Data Persistence

Market data is cached using a Docker volume:

./cache

The cache survives container rebuilds and restarts.

# Roadmap
News Headlines and Summaries  
Book Quotes/Poetry/Riddle  
Stock Scanner  
Discord Embeds  
Expanded CI/CD  
Raspberry Pi Deployment Guide  
Cron Service  

## Example Discord Webhook Integration

![Discord Integration](docs/images/discord_webhook_integration.jpg)

## Example Discord Report

![Discord Report](docs/images/discord_message_example.jpg)

## Example Docs

![Discord Report](docs/images/docs.jpg)