---
date: "2025-05-16T21:52:00+00:00"
title: "Unique Indexes: We Should Think Twice (Especially at Scale)"
categories:
  - Tech
---

In “Big Tech” environments (you know, the kind with tons of users, massive datasets, and rapidly evolving requirements), relying on database `UNIQUE INDEX` constraints to prevent duplicate data—unless it’s for something like financial reconciliation where every penny must be exact—honestly, might not be as effective as you think. Plus, the cost of maintaining them can be surprisingly high. A better approach is often to handle the bulk of deduplication logic at the application layer. If you can avoid using a database unique index, consider doing so, or at least think it through very carefully before implementing one.

# 1. Why Did I Start Rethinking Unique Indexes? Because I Got Burned.

Database unique indexes sound pretty reliable, right? The last line of defense against data duplication. I used to think so too. Whenever a field in a table needed to be unique, I’d casually slap a unique index on it.

Until reality gave me a harsh wake-up call.

A long time ago, back when my hair was much fuller, I had to add a composite unique index to a table with tens of millions of rows (say, for fields like `tenant_id` and `is_deleted` needing to be unique together). Sounds simple, doesn’t it? Well, the whole change process dragged on for days. During this time, master-slave replication lag was on a rollercoaster, and we were constantly worried about potential service hiccups. Afterwards, I couldn’t help but wonder: was this database-level “uniqueness” worth all that effort and risk?

Then there was another awkward situation. Business-wise, we all know `user@example.com` and `USER@EXAMPLE.COM` are effectively the same email. Your application code would surely normalize them (e.g., to lowercase) before checking for duplicates during registration. But the database’s unique index (which is often case-sensitive by default) doesn’t see it that way. Sometimes, due to historical data or side-channel data syncs that weren’t properly normalized, you’d end up with both case versions of the “same” email in the database. In such cases, the unique index either “turns a blind eye” to this business-level duplication or, when you try to fix the data, its rigid rules actually get in your way.

And don’t even get me started on evolving business requirements. For instance, maybe “email uniqueness” was sufficient before, but now the requirement changes to “tenant ID + email uniqueness.” Great. Application code needs to change, right? And the database’s unique index has to be `DROP` and a new one `CREATE`. How do you coordinate these two sets of operations? Which goes first? What if something goes wrong in between? Performing such operations on large tables feels like defusing a bomb every single time—utterly nerve-wracking.

These experiences forced me to ponder: in environments with large data volumes, high concurrency, and rapidly changing requirements, is the traditional approach to unique indexes still the right one? Have the drawbacks started to outweigh the benefits?

This article is about sharing my reflections on this.

# 2. `UNIQUE INDEX`: Why Do We Trust It So Much?

Before I dive into the complaints, let’s be fair and acknowledge why unique indexes are so popular. They do have several seemingly attractive points:

The ultimate safeguard for data integrity: The final barrier to prevent duplicate data.
Easy to implement: A few lines of SQL when creating a table or adding a DDL later, and you’re done.
Schema as documentation: It’s marked in the schema; this field cannot have duplicates.
A potential query performance boost: Since it’s an index, queries on this key can be faster.
These benefits are indeed quite appealing for small projects, or when data volumes are manageable and business logic isn’t overly complex. But things change dramatically when you enter the “battleground” of big data and rapid iteration.

# 3. `UNIQUE INDEX` Under the “Big Tech” Lens: Are Those Benefits Still Valid?

Let’s examine each of the “benefits” mentioned above and see if they still hold up in a large-scale, fast-paced tech environment.

- “The ultimate safeguard”? Is this safeguard reliable? What exactly is it safeguarding against?

It doesn’t fully recognize business-level “duplicates”! Except the email case sensitivity issue I mentioned earlier (which could be solved by using collation but introduce more complexity in the DB layer), or phone numbers with or without `+44`, or usernames with or without special characters stripped… these nuances, which business logic considers “the same,” are beyond the grasp of a database’s simplistic “byte-for-byte identical” unique index. It can’t prevent “logical duplicates” at the business layer.

The application layer has to do the heavy lifting anyway. Since all these complex “sameness” checks must be handled in the application code (you can’t just throw raw database errors at users, can you?), the application layer is the true workhorse ensuring “business data uniqueness.” The database’s unique index is, at best, an “auxiliary police officer” whose standards might not even align with the business rules.

In distributed systems, it’s merely a “local bodyguard.” Once you shard your tables in a distributed scenario, an in-table unique index can’t ensure global uniqueness. Global uniqueness then relies on ID generation services or application-level global validation. At this point, the “safeguard” provided by the local database index becomes even less significant.

This “ultimate safeguard” might miss the mark, has limited coverage, and relying solely on it is a bit precarious.

- “Easy to implement”? One-time setup, week-long headache.

Adding a unique index to a brand new table is indeed just one SQL statement. But more often, you’re changing the rules for an old table that’s been running for ages and has accumulated mountains of data. Trying to alter a unique index on a table with tens of millions of rows (e.g., changing from a single-field unique to a composite unique) could mean several minutes of table locking! Online DDL tools might save you from service downtime, but the entire process can still be lengthy, resource-intensive, and risky.

Agile? Not so fast! In scenarios with rapid iteration, multi-region synchronization, and compliance requirements, a single unique index change at the database level can hold you up for days. So much for agility.

So, that initial “simplicity” is like bait compared to the “hell” of modifying it later.

- “Schema as documentation”? The documentation might not match reality!

Yes, a unique index in the table structure acts as a form of “technical documentation.” But “documentation” can be misleading. If the “uniqueness” defined by this index doesn’t align with the actual, more complex business rules (like the case-insensitivity example), then this “documentation” is not only useless but can also mislead future developers. If changing this “documentation” (i.e., modifying the unique index) involves an epic struggle, why not write down the business rules properly in actual design documents, wikis, or code comments? Those are far easier to update.

- “A potential query performance boost”? Is the tail wagging the dog?

This is a common misconception, or rather, an overemphasized “added value.” If you simply want to speed up queries on a specific field or set of fields, you can absolutely create a regular, non-unique index for them! A non-unique index will boost query speeds just fine, and it comes without the write overhead, DDL pains, and rigid business logic constraints of a unique index.

- Master-slave index inconsistency can instantly “paralyze” replication:

I’ve seen it happen multiple times: the unique index configuration on the primary database is updated (e.g., a field is added, or a constraint is changed), but the index on the replica isn’t modified in sync. Then, as soon as data changes on the primary (e.g., a row is inserted that would be considered a duplicate on the replica, or the primary can write it but the replica can’t due to the incorrect/outdated index), the binlog is applied to the replica, and bam! `Slave_SQL_Running: No`. Replication just dies. When this happens, you get data lag, read-write splitting is affected, and it can even impact failover capabilities. What a nightmare, right?

# 4. Let the Application Layer Do the Job—It’s What It’s Good At!

Given all these issues with database unique indexes, the responsibility for ensuring data uniqueness should primarily fall on our application layer.

The benefits of handling uniqueness at the application layer are numerous:

- Flexible and Precise: Whatever the business defines as a duplicate, we can code the logic accordingly—case sensitivity, formatting, complex conditions, you name it.
- Better User Experience: If a user makes a mistake, we can provide clear, helpful feedback, like “This phone number is already registered. Would you like to log in instead?” rather than a cold, cryptic database error.
- Efficient Early Rejection: Intercept duplicates at the service interface layer or even the gateway layer, before the data even hits the database, saving a pointless round trip.
- Interface Idempotency: This is a powerful weapon against duplicate operations. If a user double-clicks the submit button, or a network issue causes a retry, proper idempotency at the application layer ensures data isn’t duplicated. A unique index can’t help with this.

# Conclusion

Only consider using a unique index when its benefits (usually as an absolute last-resort data backstop in extreme cases) clearly and significantly outweigh the myriad troubles it causes in complex environments with large data volumes and rapid iteration (hindering agility, operational pain). Prioritize robust application-layer uniqueness mechanisms (front-end validation, asynchronous processing, idempotency, global ID generation, etc.). As for that database unique index, avoid it if you can. If you absolutely must use one, think it through very carefully and treat it as a “specialized tool,” not a “standard configuration.”
