const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const assetsDir = path.join(__dirname, 'assets');
const images = [
  'hero_acquisition',
  'svc_google_ads',
  'svc_meta_ads',
  'svc_seo',
  'svc_cro',
  'svc_emailing',
  'svc_strategie',
  'approach_methodology'
];

(async () => {
  for (const name of images) {
    const src = path.join(assetsDir, `${name}.png`);
    const dest = path.join(assetsDir, `${name}.webp`);
    if (!fs.existsSync(src)) { console.log(`  [SKIP] ${name}.png not found`); continue; }
    await sharp(src).webp({ quality: 82 }).resize({ width: 1200, withoutEnlargement: true }).toFile(dest);
    const srcSize = (fs.statSync(src).size / 1024).toFixed(0);
    const destSize = (fs.statSync(dest).size / 1024).toFixed(0);
    console.log(`  [OK] ${name}.webp (${srcSize}KB -> ${destSize}KB, -${(100 - destSize/srcSize*100).toFixed(0)}%)`);
  }
  console.log('\nAll images converted to WebP.');
})();
