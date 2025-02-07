# Fastapi

## how to get a raw json payload

```bash
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/")
async def grafana_webhook(request: Request):
    """
    Endpoint to receive raw JSON from Grafana.
    """
    try:
        # Log the raw JSON payload
        raw_json = await request.json()
        logger.info("Received JSON payload from Grafana: %s", raw_json)

        # Return a success response
        return {"status": "success", "message": "Payload received", "data": raw_json}

    except Exception as e:
        logger.error("Error processing Grafana webhook: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))
```