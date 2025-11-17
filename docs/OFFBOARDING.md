# Talent Forge MVP - Offboarding Playbook

## Access Removal

### Repository Access
1. Remove team members from GitHub repository
2. Revoke deploy keys and personal access tokens
3. Archive repository if project is complete

### Cloud Services
1. **Vercel** (Frontend)
   - Remove team members from project
   - Archive project if no longer needed
   - Export environment variables backup

2. **Render/Fly.io** (Backend)
   - Remove team members
   - Stop services if not in use
   - Export configuration backups

3. **Database**
   - Export final database dump
   - Remove database users
   - Archive database backups

### API Keys & Secrets
1. Rotate/revoke:
   - Gemini API key
   - Google OAuth credentials
   - Database credentials
   - Any other service API keys

2. Document where keys were stored (for future reference)

## Data Handoff

### Code
- Repository is archived at: `[repository URL]`
- Main branch: `main`
- Latest tag: `v1.0`

### Documentation
- System design: `docs/SYSTEM_DESIGN_ONE_PAGER.md`
- API contract: `docs/API_CONTRACT.md`
- This offboarding doc: `docs/OFFBOARDING.md`

### Database
- Export location: `[backup location]`
- Schema: See `api/app/models.py`
- Migrations: `api/alembic/versions/`

### Fixtures & Test Data
- Location: `fixtures/`
- Includes: Sample resumes, JDs, expected outputs

## Knowledge Transfer

### Key Contacts
- **Project Lead**: [Name/Email]
- **Technical Lead**: [Name/Email]

### Architecture Decisions
- See `docs/SYSTEM_DESIGN_ONE_PAGER.md`
- API contract: `openapi/talent-forge.v1.yaml`

### Known Issues & Limitations
- Auth is stubbed (not production-ready)
- No rate limiting on analyze endpoint
- Embedding cache is in-memory (not persistent)
- Database migrations need to be run manually

## Acknowledgments

Thank you to all team members who contributed to this MVP:
- [List team members]

## Next Steps (if continuing)

1. Implement production auth (Google OAuth)
2. Add rate limiting
3. Implement persistent caching
4. Add monitoring/observability
5. Scale database for production load
