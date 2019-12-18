CREATE TABLE pictures (
  [id] int PRIMARY KEY IDENTITY,
  [name] varchar(255),
  [user] varchar(255),
  [timestamp] datetime2,
  [img] varbinary(max)
);

CREATE TABLE clouds (
  [id] int PRIMARY KEY IDENTITY,
  [name] varchar(255),
  [img] varbinary(max),
  [machine] varchar(255),
  [approved] varchar(255)
);

CREATE TABLE logs (
  [id] int,
  [command] varchar(255),
  [timestamp] datetime2,
  [user] varchar(255)
);

ALTER TABLE dbo.logs
DROP COLUMN ID;
ALTER TABLE dbo.logs
   ADD ID INT IDENTITY
       CONSTRAINT PK_logs PRIMARY KEY CLUSTERED;