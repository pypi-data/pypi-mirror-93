// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { 
    getCellSelector,
} from '../utils/selectors';

import { 
    checkColumn,
    tryTest,
} from '../utils/helpers';
import { Selector } from 'testcafe';

import {
    addColumnButton,
    setFormula
} from '../utils/columnHelpers';

import { CURRENT_URL } from '../config';

const code = "import pandas as pd\nimport mitosheet\ndf = pd.DataFrame(data={'day': [1, 2, 3, 4, 5, 6, 7, 8], 'score': [-100, -50, 0, 10, 61, 100, 151, 1000]})\nmitosheet.sheet(df)";

fixture `Test Rolling Window`
    .page(CURRENT_URL)

test('Can create a rolling window function without clicking', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await t.click(addColumnButton)
            await setFormula(t, '=IF(score - OFFSET(score, -1) > 50, 1, 0)', 'C', '0');
            await checkColumn(t, 'C', ['0', '0', '0', '0', '1', '0', '1', '1'])
        }
    )
});

test('Can create a rolling window function by clicking', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await t.click(addColumnButton)

            // Start in the second row
            const cell = getCellSelector('C', '1');

            await t
                .click(cell)
                .pressKey('enter')
                .selectText(Selector('input.ag-cell-inline-editing'))
                .pressKey('delete+delete') 
                .typeText(Selector('input.ag-cell-inline-editing'), '=IF(score - ')
                // Click a row up
                .click(getCellSelector('score', '0'))
                // Finish the formula
                .typeText(Selector('input.ag-cell-inline-editing'), '> 50, 1, 0)')
                .pressKey('enter')


            await checkColumn(t, 'C', ['0', '0', '0', '0', '1', '0', '1', '1'])
        }
    )
});