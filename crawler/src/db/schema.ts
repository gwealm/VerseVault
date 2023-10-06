import { sql } from 'drizzle-orm';
import * as dz from 'drizzle-orm/sqlite-core';

export const artists = dz.sqliteTable("artists", {
    id: dz.integer("id").primaryKey(),
    createdAt: dz.integer("created_at", { mode: 'timestamp' })
        .default(sql`CURRENT_TIMESTAMP`),
    // mbid: dz.text("mbid"),
    name: dz.text("name").notNull(),
    visited: dz.integer("visited", { mode: "boolean" })
        .default(false)
});

export const albums = dz.sqliteTable("artists", {
    id: dz.integer("id").primaryKey(),
    createdAt: dz.integer("created_at", { mode: 'timestamp' })
        .default(sql`CURRENT_TIMESTAMP`),
    // mbid: dz.text("mbid"),
    name: dz.text("name").notNull(),
    artist: dz.text("artist").notNull(),
    visited: dz.integer("visited", { mode: "boolean" })
    .default(false)
});

export const tracks = dz.sqliteTable("tracks", {
    id: dz.integer("tracks").primaryKey(),
    createdAt: dz.integer("created_at", { mode: 'timestamp' })
        .default(sql`CURRENT_TIMESTAMP`),
    // mbid: dz.text("mbid"),
    name: dz.text("name").notNull(),
    artist: dz.text("artist").notNull(),
    visited: dz.integer("visited", { mode: "boolean" })
        .default(false),
});