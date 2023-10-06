import * as path from "node:path";

const WORKER_PATH = path.join(__dirname, "worker.ts");
const WORKER_NUM = 8

const workers: Worker[] = []
const availability: boolean[] = []

function main() {
    // Create workers
    for (let i = 0; i < WORKER_NUM; i++) {
        const worker = new Worker(WORKER_PATH, {
            name: `crawler#${i}`,
            type: "module",
        });
    
        workers.push(worker);
        availability.push(true);
    }

    for (const i in workers) {
        const worker = workers[i];

        worker.addEventListener("message", (ev) => {
            const message = ev.data;

            if (message === "status:available") {
                availability[i] = true
            }
        })
    }
}

async function processCommand(command: unknown) {
    return new Promise((resolve, reject) => {
        for (const worker of workers) {
            
        }
    });
    for (const worker of )
} 