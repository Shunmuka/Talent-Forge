-- Talent Forge MVP - Database Bootstrap Script
-- This script initializes the database schema

-- Create database if it doesn't exist (run as postgres user)
-- CREATE DATABASE talent_forge;

-- Connect to talent_forge database
-- \c talent_forge;

-- Note: Tables will be created by Alembic migrations
-- Run: alembic upgrade head

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The following tables will be created by SQLAlchemy models via Alembic:
-- - users
-- - resumes
-- - analyses
-- - bullet_rewrites
