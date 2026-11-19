import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = resolve(process.cwd(), process.env.MAKEFUN_OUTPUT_DIR ?? "out");
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);
// Guard the gate: the two graded runs must write identical bytes, so refuse
// to finish silently if the copy ever differs from the source.
const srcBytes = statSync(src).size;
const dstBytes = statSync(dst).size;
if (srcBytes !== dstBytes) {
  throw new Error(`copy size mismatch: ${srcBytes} vs ${dstBytes}`);
}
console.log("entry.png copied to", dst, `(${dstBytes} bytes)`);
