# 🔍 Astra Watchdog Monitoring System

The Astra Watchdog is a real-time monitoring and alerting system that enhances the bot detection capabilities by continuously monitoring sessions, detecting suspicious patterns, and providing proactive alerts.

## 🚀 Features

### **Real-time Monitoring**
- **Session Analysis**: Monitors every session processed by the Astra API
- **Pattern Detection**: Identifies suspicious behavioral patterns
- **Rate Limiting**: Tracks and limits rapid requests from single IPs
- **Anomaly Detection**: Detects unusual patterns across multiple sessions

### **Alert System**
- **High Confidence Bot Alerts**: Triggers when bot detection confidence > 95%
- **Rapid Request Alerts**: Warns about excessive requests per minute
- **Burst Attack Detection**: Identifies sudden bursts of requests
- **Suspicious Behavior Alerts**: Flags unusual behavioral patterns

### **IP Management**
- **Suspicious IP Tracking**: Monitors IPs with suspicious activity
- **Automatic Blocking**: Blocks IPs after multiple violations
- **Violation Counting**: Tracks violation counts per IP

### **Statistics & Analytics**
- **Real-time Metrics**: Live statistics on sessions, bots, and alerts
- **Historical Data**: Maintains session and alert history
- **Export Capabilities**: Export monitoring data for analysis

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client Apps   │───▶│  Astra Backend  │───▶│   Watchdog      │
│                 │    │   (FastAPI)     │    │   Monitor       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   ML Model      │    │   Alert Log     │
                       │   (Random       │    │   & Statistics  │
                       │    Forest)      │    │                 │
                       └─────────────────┘    └─────────────────┘
```

## 📊 API Endpoints

### **Core Prediction Endpoint**
```http
POST /predict
```
Enhanced with watchdog monitoring - returns alerts if suspicious activity detected.

### **Watchdog Monitoring Endpoints**
```http
GET /watchdog/stats          # Get monitoring statistics
GET /watchdog/alerts         # Get recent alerts
GET /watchdog/suspicious-ips # Get suspicious IPs
POST /watchdog/export        # Export monitoring data
```

## 🎯 Alert Types

| Alert Type | Severity | Description | Threshold |
|------------|----------|-------------|-----------|
| `HIGH_CONFIDENCE_BOT` | CRITICAL | Bot detected with >95% confidence | 0.95 |
| `RAPID_REQUESTS` | WARNING | Too many requests per minute | 10/min |
| `BURST_ATTACK` | HIGH | Sudden burst of requests | 5/10sec |
| `SUSPICIOUS_BEHAVIOR` | MEDIUM | Unusual behavioral patterns | Custom |

## 🚀 Getting Started

### **1. Start the Backend with Watchdog**
```bash
cd astra/src
uvicorn backend:app --reload
```
The watchdog automatically starts when the backend loads.

### **2. Run the Watchdog Dashboard**
```bash
cd astra/app
streamlit run watchdog_dashboard.py
```

### **3. Test the Watchdog System**
```bash
cd astra
python test_watchdog.py
```

## 📈 Dashboard Features

### **Real-time Statistics**
- Total sessions processed
- Bots detected and detection rate
- Alerts triggered
- Suspicious IPs count
- System uptime

### **Live Alerts Panel**
- Color-coded alerts by severity
- Real-time alert updates
- Alert details and timestamps

### **Suspicious IP Management**
- IP violation tracking
- Automatic status updates
- Visual charts and graphs

### **Analytics & Charts**
- Bot detection rate gauge
- Alert history analysis
- IP violation trends

## 🔧 Configuration

### **Anomaly Thresholds**
```python
anomaly_thresholds = {
    'high_confidence_bot': 0.95,    # Bot confidence threshold
    'rapid_requests': 10,           # Requests per minute
    'suspicious_pattern': 0.8,      # Suspicious pattern threshold
    'burst_threshold': 5            # Requests in 10 seconds
}
```

### **Rate Limiting**
- **Warning**: >10 requests/minute
- **Blocking**: >20 requests/minute (3 violations)
- **Cleanup**: Old data removed after 5 minutes

## 📝 Logging

The watchdog system logs all activities to:
- **Console**: Real-time monitoring output
- **File**: `logs/watchdog.log` for persistent logging
- **API**: Structured data via REST endpoints

### **Log Levels**
- `INFO`: Normal operations and statistics
- `WARNING`: Suspicious activity detected
- `ERROR`: System errors and failures

## 🔍 Monitoring Scenarios

### **Normal Traffic**
- Human users with realistic behavior
- No alerts triggered
- Normal detection rates

### **Bot Attack**
- Automated requests with bot-like patterns
- High confidence bot alerts
- Rate limiting warnings

### **Burst Attack**
- Sudden surge of rapid requests
- Burst attack alerts
- IP blocking after violations

### **Suspicious Behavior**
- Unusual patterns (perfect form filling, etc.)
- Behavioral alerts
- Pattern analysis

## 📊 Data Export

Export monitoring data for analysis:
```bash
curl -X POST http://localhost:8000/watchdog/export
```

Exported data includes:
- Statistics summary
- Recent alerts
- Suspicious IPs
- Timestamp information

## 🛠️ Integration

### **With Existing Astra System**
The watchdog integrates seamlessly with the existing Astra bot detection system:

1. **Automatic Integration**: No changes needed to existing API calls
2. **Enhanced Responses**: API responses include alerts when detected
3. **Backward Compatibility**: All existing functionality preserved

### **Custom Integration**
```python
from watchdog import get_watchdog

# Get watchdog instance
watchdog = get_watchdog()

# Process session with monitoring
result = watchdog.process_session(session_data, client_ip)

# Check for alerts
if result.get('alerts'):
    for alert in result['alerts']:
        print(f"Alert: {alert['type']} - {alert['message']}")
```

## 🔒 Security Features

### **IP-based Protection**
- Automatic blocking of malicious IPs
- Violation tracking and escalation
- Configurable blocking thresholds

### **Rate Limiting**
- Per-IP request tracking
- Automatic cleanup of old data
- Configurable rate limits

### **Alert Escalation**
- Multiple severity levels
- Automatic notification system
- Historical alert tracking

## 📈 Performance

### **Memory Management**
- Limited history storage (1000 sessions, 100 alerts)
- Automatic cleanup of old data
- Efficient data structures

### **Scalability**
- Thread-safe operations
- Minimal impact on API performance
- Configurable resource limits

## 🚨 Troubleshooting

### **Common Issues**

1. **Watchdog not starting**
   - Check if backend API is running
   - Verify model files exist
   - Check logs for errors

2. **No alerts being triggered**
   - Verify anomaly thresholds
   - Check session data format
   - Review log files

3. **High memory usage**
   - Reduce history limits
   - Increase cleanup frequency
   - Monitor session volume

### **Debug Mode**
Enable detailed logging:
```python
import logging
logging.getLogger('watchdog').setLevel(logging.DEBUG)
```

## 🔮 Future Enhancements

### **Planned Features**
- **Machine Learning Alerts**: ML-based anomaly detection
- **Geographic Blocking**: Country-based IP blocking
- **Advanced Analytics**: Predictive threat analysis
- **Integration APIs**: Third-party security tool integration

### **Customization Options**
- **Custom Alert Rules**: User-defined alert conditions
- **Notification System**: Email/SMS alerts
- **Dashboard Customization**: Configurable widgets
- **Data Retention**: Configurable history limits

## 📚 API Documentation

For complete API documentation, visit:
```
http://localhost:8000/docs
```

The watchdog endpoints are documented in the FastAPI auto-generated docs.

---

**🔍 Astra Watchdog** - Proactive bot detection monitoring for the modern web. 