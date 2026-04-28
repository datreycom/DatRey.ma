const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'assets');
const files = fs.readdirSync(dir).filter(f => f.endsWith('.png'));

(async () => {
  for (const file of files) {
    const src = path.join(dir, file);
    const dst = path.join(dir, file.replace('.png', '.webp'));
    const info = await sharp(src)
      .webp({ quality: 80 })
      .toFile(dst);
    const oldSize = fs.statSync(src).size;
    console.log(`${file} → ${file.replace('.png','.webp')}  ${(oldSize/1024).toFixed(0)}KB → ${(info.size/1024).toFixed(0)}KB  (-${(100-info.size/oldSize*100).toFixed(0)}%)`);
    fs.unlinkSync(src); // Remove original PNG
  }
  console.log('Done! All images converted to WebP.');
})();
