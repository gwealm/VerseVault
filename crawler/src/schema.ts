import { z } from "zod";

export const message = z.object({
    kind: z.enum(["main:assign", "worker:result", "worker:error"])
})

export const workloadAssignedMessage = z.object({
    kind: z.literal("main:assign"),
    workload: z.union([
        z.object({
            type: z.enum(["track", "album"]),
            artist: z.string(),
            name: z.string(),
        }),
        z.object({
            type: z.literal("artist"),
            name: z.string(),
        })
    ])
});

export const workerResultMessage = z.object({
    kind: z.literal("worker:result")
})