const { readdir, readFile, writeFile } = require('fs').promises;

const getDirectories = async (source) =>
  (await readdir(source, { withFileTypes: true }))
    .filter((dirent) => dirent.isDirectory())
    .map((dirent) => dirent.name);

let count = 0;
const run = async () => {
  const dirs = await getDirectories('./');

  for await (const name of dirs) {
    if (name !== 'node_modules' && name !== '.git') {
      const dir = await readdir(name, {});

      await Promise.all(
        dir.map(async (file) => {
          const content = await readFile(__dirname + `/${name}/${file}`, 'utf8');
          try {
            const json = JSON.parse(content);
            const entries =
              json.data.search_by_raw_query.search_timeline.timeline.instructions[0].entries;
            count += entries.length;
            // console.log(`${name}/${__dirname + `/${name}/$`}: ${count}`);
          } catch (error) {
            console.log(`${name}/${__dirname + `/${name}/${file}`}: ${error}}`);
          }
        })
      );
    }
  }

  // Edit README.md to update the count

  const readme = await readFile(__dirname + '/README.md', 'utf8');
  const lines = readme.split('\n');
  const countLine = lines.find((line) => line.includes('Total tweets'));
  const newCountLine = countLine.replace(/\d+/, count);
  const newReadme = readme.replace(countLine, newCountLine);
  await writeFile(__dirname + '/README.md', newReadme, 'utf8');
};

run();
