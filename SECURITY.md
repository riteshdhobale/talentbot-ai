# Security Notes

## ⚠️ Important Security Reminders

### API Key Security

Your OpenAI API key has been added to `backend/.env`. Please note:

1. **Never commit `.env` files to Git**
   - The `.gitignore` file already excludes `.env` files
   - Always verify before pushing to GitHub

2. **Rotate keys if exposed**
   - If you accidentally commit your key, rotate it immediately in OpenAI dashboard
   - Old key: `sk-proj-vLFVaxbCRPin8VxZehQyb...` (truncated for security)

3. **Use environment variables in production**
   - Don't hardcode keys in code
   - Use secure secret management (Railway secrets, Render env vars, etc.)

4. **Monitor API usage**
   - Check OpenAI dashboard regularly for unexpected usage
   - Set up usage alerts if available

### Best Practices

- ✅ `.env` files are in `.gitignore`
- ✅ Never share API keys in screenshots or messages
- ✅ Use different keys for development and production
- ✅ Rotate keys periodically

### If Key is Compromised

1. Go to https://platform.openai.com/api-keys
2. Delete the compromised key
3. Create a new key
4. Update `backend/.env` with the new key

