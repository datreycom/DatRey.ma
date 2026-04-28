const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

const brainDir = 'C:\\Users\\Omar\\.gemini\\antigravity\\brain\\3f75449c-0470-4fef-8dc1-254adcac58c0';
const assetsDir = path.join(__dirname, 'assets');

// Find the files dynamically
const files = fs.readdirSync(brainDir);

const transfoImg = files.find(f => f.startsWith('transfo_digitale_hero') && f.endsWith('.png'));
const contactImg = files.find(f => f.startsWith('contact_hero') && f.endsWith('.png'));

if (!transfoImg || !contactImg) {
    console.error('Could not find generated images in brain directory');
    process.exit(1);
}

async function convert() {
    console.log('Converting transfo digitale hero...');
    await sharp(path.join(brainDir, transfoImg))
        .resize(1200, 675, { fit: 'cover', position: 'center' })
        .webp({ quality: 85, effort: 6 })
        .toFile(path.join(assetsDir, 'transfo_digitale_hero.webp'));
        
    console.log('Converting contact hero...');
    await sharp(path.join(brainDir, contactImg))
        .resize(1200, 675, { fit: 'cover', position: 'center' })
        .webp({ quality: 85, effort: 6 })
        .toFile(path.join(assetsDir, 'contact_hero.webp'));
        
    console.log('Conversion complete!');
}

convert().catch(console.error);
