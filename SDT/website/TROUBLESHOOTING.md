# Troubleshooting Guide

## Rollup Native Module Issue

If you're getting the `@rollup/rollup-win32-x64-msvc` error, try these steps:

### Solution 1: Clean Reinstall
```powershell
cd SDT\website
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json
npm cache clean --force
npm install
npm install @rollup/rollup-win32-x64-msvc@4.54.0 --save
npm run dev
```

### Solution 2: Manual Installation
```powershell
cd SDT\website
npm install @rollup/rollup-win32-x64-msvc@4.54.0 --save-exact
npm run dev
```

### Solution 3: Use npm ci
```powershell
cd SDT\website
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json
npm install
npm ci
npm run dev
```

### Solution 4: Check Node Version
```powershell
node --version
```
Should be Node 18+ for Astro 4.x

### Solution 5: Alternative - Use Vite Directly
If Rollup continues to fail, we can configure Astro to use Vite's bundler instead.

---

## Current Status

The dev server should be starting. Check the terminal output for:
- `Local: http://localhost:4321/`
- Any error messages

If you see errors, share them and we'll fix them!

