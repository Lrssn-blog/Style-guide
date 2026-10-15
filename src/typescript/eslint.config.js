import eslint from '@eslint/js';
import {defineConfig} from 'eslint/config';
import tseslint from 'typescript-eslint';

export default defineConfig(
        eslint.configs.recommended,
        tseslint.configs.strictTypeChecked,
        tseslint.configs.stylisticTypeChecked,
        {
            languageOptions: {
                parserOptions: {
                    projectService: true,
                    tsconfigRootDir: import.meta.dirname,
                },
            },
            rules: {
                '@typescript-eslint/consistent-type-imports': 'error',
                '@typescript-eslint/explicit-module-boundary-types': 'error',
                'no-restricted-syntax': ['error', 'ExportDefaultDeclaration'],
            },
        },
);
