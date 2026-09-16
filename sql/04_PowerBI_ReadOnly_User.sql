-- Run in the target database and replace the placeholder securely.
-- For production, prefer your organization's approved Entra/managed identity approach.
CREATE USER powerbi_reader WITH PASSWORD = '<strong-password-not-stored-in-git>';
ALTER ROLE db_datareader ADD MEMBER powerbi_reader;
