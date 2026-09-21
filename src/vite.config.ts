import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import { viteStaticCopy } from 'vite-plugin-static-copy';

export default defineConfig({
    base: "/static/",
    plugins: [
        tailwindcss(),

        viteStaticCopy({
            targets: [
                {
                    src: 'node_modules/flowbite/dist/flowbite.min.js',
                    dest: 'quinzobase/js',
                    rename: {
                        stripBase: true,
                    },
                },
            ],
        }),
    ],

    build: {
        rollupOptions: {
            input: {
                output: './quinzo/static/quinzobase/css/input.css',
            },

            output: {
                assetFileNames: (assetInfo) => {
                    const name = assetInfo.names[0] ?? '';

                    if (/\.(woff2?|ttf|otf|eot)$/.test(name)) {
                        return 'webfonts/[name][extname]';
                    }

                    if (name.endsWith('.css')) {
                        return 'quinzobase/css/[name][extname]';
                    }

                    return 'quinzobase/assets/[name][extname]';
                },
            },
        },

        outDir: './quinzo/static.dist',
        emptyOutDir: true,
    },
});