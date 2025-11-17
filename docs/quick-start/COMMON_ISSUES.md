# Common Issues & Solutions

## 🔴 Backend Issues

### "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
cd api
pip install -e . && pip install -e ".[dev]"
```

### "Address already in use" (Port 8000)

**Solution:**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill

# Or use a different port
uvicorn app.main:app --port 8001
```

### "GEMINI_API_KEY not found"

**Solution:**
1. Create `.env` file in project root
2. Add: `GEMINI_API_KEY=your-key-here`
3. Restart backend server

### "Failed to import ml.scorer"

**Solution:**
```bash
# Make sure PYTHONPATH includes project root
export PYTHONPATH=/path/to/Talent-Forge:$PYTHONPATH

# Or run from project root
cd /path/to/Talent-Forge
PYTHONPATH=. uvicorn api.app.main:app --reload
```

---

## 🔴 Frontend Issues

### "npm: command not found"

**Solution:**
- Install Node.js from https://nodejs.org/
- Or use Homebrew: `brew install node`

### "Port 3000 already in use"

**Solution:**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill

# Or use different port
PORT=3001 npm run dev
```

### "Module not found" errors

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### "Failed to fetch" when uploading files

**Solution:**
1. Check backend is running on port 8000
2. Check browser console for CORS errors
3. Verify file format (PDF, DOCX, TXT)
4. Check file size (must be < 16MB)

---

## 🔴 API Key Issues

### Still seeing "API Configuration" gaps

**Check:**
1. `.env` file exists in project root
2. `GEMINI_API_KEY=your-key` is in `.env`
3. Backend was restarted after adding key
4. No typos in API key

**Solution:**
```bash
# Verify .env
cat .env | grep GEMINI_API_KEY

# Restart backend
pkill -f uvicorn
# Then start again
```

### "API not configured" in rewrite

**Solution:**
- Same as above - verify API key is set and backend restarted

---

## 🔴 Database Issues (Optional)

### "Could not connect to database"

**Solution:**
- Database is optional for MVP
- Comment out database imports if not using
- Or start PostgreSQL: `docker-compose up -d postgres`

---

## 🟡 Performance Issues

### Slow analysis (>10 seconds)

**Possible causes:**
- First run (downloading ML models)
- Large resume/JD files
- Network issues with Gemini API

**Solution:**
- Wait for first run to complete (downloads models)
- Reduce input size
- Check internet connection

---

## 🟢 Quick Fixes

### Reset Everything

```bash
# Stop all servers
pkill -f uvicorn
pkill -f "next dev"

# Reinstall dependencies
cd api && pip install -e . && cd ..
cd frontend && npm install && cd ..

# Restart
make dev
```

### Check Server Status

```bash
# Backend
curl http://localhost:8000/healthz

# Frontend
curl http://localhost:3000
```

### View Logs

```bash
# Backend logs (if using background process)
tail -f /tmp/backend.log

# Frontend logs (check terminal where npm run dev is running)
```

---

## 📞 Still Having Issues?

1. Check all prerequisites are installed
2. Verify `.env` file is configured
3. Check server logs for errors
4. Make sure ports 3000 and 8000 are available
5. Try restarting both servers

