// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import { FilterObjectArray } from "./components/taskpanes/ControlPanel/FilterCard";
import { SortDirection } from "./components/taskpanes/ControlPanel/SortCard";
import { AggregationType } from "./components/taskpanes/PivotTable/PivotTaskpane";


/*
  Contains a wrapper around a strongly typed object that simulates a web-api. 
*/

// Max delay is the longest we'll wait for the API to return a value
const MAX_DELAY = 5000;
// How often we poll to see if we have a response yet
const RETRY_DELAY = 250;
const MAX_RETRIES = MAX_DELAY / RETRY_DELAY;


const getRandomId = (): string => {
    return '_' + Math.random().toString(36).substr(2, 9);
}

// NOTE: these have pythonic field names because we parse their JSON directly in the API
export interface SimpleImportSummary {
    step_type: 'simple_import';
    file_names: string[];
}
export interface RawPythonImportSummary {
    step_type: 'raw_python_import';
    python_code: string;
    new_df_names: string[];
}

export interface ImportSummaries {
    [key: string]: SimpleImportSummary | RawPythonImportSummary
}

/*
  The MitoAPI class contains functions for interacting with the Mito backend. All 
  interactions with the backend should go through this call, so that if we ever move
  to a more standard API, the migration is protected by this interface!
*/
export class MitoAPI {
    send: (msg: Record<string, unknown>) => void;
    unconsumedResponses: Record<string, unknown>[];

    constructor(send: (msg: Record<string, unknown>) => void) {
        this.send = send;
        this.unconsumedResponses = [];
    }

    /*
        The receive response function is a workaround to the fact that we _do not_ have
        a real API in practice. If/when we do have a real API, we'll get rid of this function, 
        and allow the API to just make a call to a server, and wait on a response
    */
    receiveResponse(response: Record<string, unknown>): void {
        this.unconsumedResponses.push(response);
    }

    /*
        Helper function that tries to get the response for a given ID, and returns
        the data inside the 'data' key in this response if it exists. 

        Returns undefined if it does not get a response within the set timeframe
        for retries.
    */
    getResponseData(id: string): Promise<unknown | undefined> {
    
        return new Promise((resolve) => {
            let tries = 0;
            const interval = setInterval(() => {
                // Only try at most MAX_RETRIES times
                tries++;
                if (tries > MAX_RETRIES) {
                    clearInterval(interval);
                    // If we fail, we return an empty response
                    return resolve(undefined)
                }

                // See if there is an API response to this one specificially
                const index = this.unconsumedResponses.findIndex((response) => {
                    return response['id'] === id;
                })
                if (index !== -1) {
                    // Clear the interval
                    clearInterval(interval);

                    const response = this.unconsumedResponses[index];
                    this.unconsumedResponses.splice(index, 1);
          
                    return resolve(response['data']); // return to end execution
                } else {
                    console.log("Still waiting")
                }
            }, RETRY_DELAY);
        })
    }

    /*
        Returns all the CSV files in the current folder as the kernel.
    */
    async getDataFiles(): Promise<string[]> {
        const id = getRandomId();

        this.send({
            'event': 'api_call',
            'type': 'datafiles',
            'id': id
        })

        const dataFiles = await this.getResponseData(id) as string[] | undefined;
    
        if (dataFiles == undefined) {
            return []
        }
        return dataFiles;
    }

    /*
        Import summaries are a mapping from step_idx -> import information for each of the 
        import steps in the analysis with the given analysisName.
    */
    async getImportSummary(analysisName: string): Promise<ImportSummaries> {
        const id = getRandomId();

        this.send({
            'event': 'api_call',
            'type': 'import_summary',
            'id': id,
            'analysis_name': analysisName
        })

        const importSumary = await this.getResponseData(id) as ImportSummaries | undefined;
    
        if (importSumary == undefined) {
            return {}
        }
        return importSumary;
    }

    /*
        Adds a column with the passed parameters
    */
    async sendColumnAddMessage(
        sheetIndex: number,
        columnHeader: string,
        stepID?: string
    ): Promise<string> {
        if (stepID === undefined || stepID == '') {
            stepID = getRandomId();
        }

        this.send({
            'event': 'edit_event',
            'type': 'add_column_edit',
            'sheet_index': sheetIndex,
            'column_header': columnHeader
        })

        return stepID;
    }

    /*
        Adds a delete column message with the passed parameters
    */
    async sendDeleteColumn(
        sheetIndex: number,
        columnHeader: string,
    ): Promise<void> {
        this.send({
            'event': 'edit_event',
            'type': 'delete_column_edit',
            'sheet_index': sheetIndex,
            'column_header': columnHeader
        })
    }

    /*
        Does a merge with the passed parameters, returning the ID of the edit
        event that was generated (in case you want to overwrite it).
    */
    async sendMergeMessage(
        sheetOneIndex: number,
        sheetOneMergeKey: string,
        sheetOneSelectedColumns: string[],
        sheetTwoIndex: number,
        sheetTwoMergeKey: string,
        sheetTwoSelectedColumns: string[],
        /* 
            If you want to overwrite, you have to pass the ID of the the step that
            you want to overwrite. Not passing this argument, or passing an empty string,
            will result in no overwrite occuring (and a new stepID) being returned.
        */
        stepID?: string
    ): Promise<string> {
        // If this is overwriting a merge event, then we do not need to
        // create a new id, as we already have it!
        if (stepID === undefined || stepID == '') {
            stepID = getRandomId();
        }

        this.send({
            event: 'edit_event',
            type: 'merge_edit',
            step_id: stepID,
            sheet_index_one: sheetOneIndex,
            merge_key_one: sheetOneMergeKey,
            selected_columns_one: sheetOneSelectedColumns,
            sheet_index_two: sheetTwoIndex,
            merge_key_two: sheetTwoMergeKey,
            selected_columns_two: sheetTwoSelectedColumns,
        })

        return stepID;
    }

    /*
        Does a pivot with the passed parameters, returning the ID of the edit
        event that was generated (in case you want to overwrite it).
    */
    async sendPivotMessage(
        sheetIndex: number,
        pivotRows: string[],
        pivotCols: string[],
        values: Record<string, AggregationType>,
        stepID?: string
    ): Promise<string> {
        // If this is overwriting a pivot event, then we do not need to
        // create a new id, as we already have it!
        if (stepID === undefined || stepID === '') {
            stepID = getRandomId();
        }

        this.send({
            event: 'edit_event',
            type: 'pivot_edit',
            sheet_index: sheetIndex,
            pivot_rows: pivotRows,
            pivot_columns: pivotCols,
            values: values, 
            step_id: stepID
        });

        return stepID;
    }

    /*
        Reorders the columnHeader on sheetIndex to the newIndex, and shifts the remaining
        columns to the right.
    */
    async sendReorderColumnMessage(
        sheetIndex: number,
        columnHeader: string,
        newIndex: number
    ): Promise<void> {
        this.send({
            'event': 'edit_event',
            'type': 'reorder_column_edit',
            'sheet_index': sheetIndex,
            'column_header': columnHeader,
            'new_column_index': newIndex
        });
    }

    /*
        Renames the dataframe at sheetIndex.
    */
    async sendDataframeRenameEdit(
        sheetIndex: number,
        newDataframeName: string,
        stepID?: string,
    ): Promise<string> {
        // If this is overwriting a pivot event, then we do not need to
        // create a new id, as we already have it!
        if (stepID === undefined || stepID === '') {
            stepID = getRandomId();
        }

        this.send({
            'event': 'edit_event',
            'type': 'dataframe_rename_edit',
            'sheet_index': sheetIndex,
            'new_dataframe_name': newDataframeName
        })

        return stepID;
    }

    /*
        Does a filter with the passed parameters, returning the ID of the edit
        event that was generated (in case you want to overwrite it).
    */
    async sendFilterMessage(
        sheetIndex: number,
        columnHeader: string,
        filters: FilterObjectArray,
        operator: 'And' | 'Or',
        stepID?: string    
    ): Promise<string> {
        // create a new id, if we need it!
        if (stepID === undefined || stepID === '') {
            stepID = getRandomId();
        }

        this.send({
            event: 'edit_event',
            type: 'filter_column_edit',
            sheet_index: sheetIndex,
            column_header: columnHeader,
            operator: operator,
            filters: filters,
            step_id: stepID

        });
        return stepID;
    }

    /*
        Does a sort with the passed parameters, returning the ID of the edit
        event that was generated (in case you want to overwrite it).
    */
    async sendSortMessage(
        sheetIndex: number,
        columnHeader: string,
        sortDirection: SortDirection,
        stepID?: string    
    ): Promise<string> {
        if (stepID === undefined || stepID === '') {
            stepID = getRandomId();
        }

        this.send({
            event: 'edit_event',
            type: 'sort_edit',
            sheet_index: sheetIndex,
            column_header: columnHeader,
            sort_direction: sortDirection,
            step_id: stepID
        });

        return stepID;
    }

    /*
        Renames a column with the passed parameters
    */
    async sendRenameColumn(
        sheetIndex: number,
        oldColumnHeader: string,
        newColumnHeader: string,
        stepID?: string
    ): Promise<string> {
        if (stepID === undefined || stepID === '') {
            stepID = getRandomId();
        }

        this.send({
            event: 'edit_event',
            type: 'rename_column_edit',
            sheet_index: sheetIndex,
            old_column_header: oldColumnHeader,
            new_column_header: newColumnHeader,
            stepID: stepID
        });

        return stepID;
    }

    /*
        Duplicates the dataframe at sheetIndex.
    */
    async sendDataframeDuplicateMessage(
        sheetIndex: number
    ): Promise<void> {
        this.send({
            'event': 'edit_event',
            'type': 'dataframe_duplicate_edit',
            'sheet_index': sheetIndex,
        })
    }

    /*
        Deletes the dataframe at the passed sheetIndex
    */
    async sendDataframeDeleteMessage(
        sheetIndex: number
    ): Promise<void> {
        this.send({
            'event': 'edit_event',
            'type': 'dataframe_delete_edit',
            'sheet_index': sheetIndex,
        })
    }

    /*
        Sends an undo message, which removes the last step that was created. 
    */
    async sendUndoMessage(): Promise<void> {
        this.send({
            'event': 'update_event',
            'type': 'undo'
        })
    }

    /*
        Sends a message which saves the current analysis with the passed
        analysisName. 
    */
    async sendSaveAnalysisMessage(
        analysisName: string
    ): Promise<void> {
        this.send({
            'event': 'update_event',
            'type': 'save_analysis_update',
            'analysis_name': analysisName
        });
    }

    /*
        Sends a message to tell Mito to replay an existing analysis onto
        the current analysis.
    */
    async sendUseExistingAnalysisUpdateMessage(
        analysisName: string,
        newFileNames?: ImportSummaries,
        clearExistingAnalysis?: boolean
    ): Promise<void> {
        
        this.send({
            'event': 'update_event',
            'type': 'replay_analysis_update',
            'analysis_name': analysisName,
            'import_summaries': newFileNames === undefined ? {} : newFileNames,
            'clear_existing_analysis': clearExistingAnalysis === undefined ? false : clearExistingAnalysis
        });
    }

    /*
        Sets the formula for the given columns.
    */
    async sendSetColumnFormulaEditMessage(
        sheetIndex: number,
        columnHeader: string,
        newFormula: string,
    ): Promise<void> {
        this.send({
            'event': 'edit_event',
            'type': 'set_column_formula_edit',
            'sheet_index': sheetIndex,
            'column_header': columnHeader,
            'new_formula': newFormula
        });
    }

    /*
        Imports the given file names.
    */
    async sendSimpleImportMessage(
        fileNames: string[],
    ): Promise<void> {
        this.send({
            'event': 'edit_event',
            'type': 'simple_import_edit',
            'file_names': fileNames,
        })
    }

    /*
        Does an import by running the pythonCode, and pulling out
        the new df names.
    */
    async sendRawPythonImportMessage(
        pythonCode: string,
        newDfNames: string[]
    ): Promise<void> {
        this.send({
            'event': 'edit_event',
            'type': 'raw_python_import_edit',
            'python_code': pythonCode,
            'new_df_names': newDfNames,
        })
    }

    /*
        Sends a log event from the frontend to the backend, where it is logged
        by the backend. We log in the backend to keep a linear stream of actions 
        that is making.
    */
    async sendLogMessage(
        logEventType: string,
        params?: Record<string, unknown>
    ): Promise<void> {

        let message: Record<string, unknown> = {};
        // Copy the params, so we don't accidently modify anything
        if (params !== undefined) {
            message = Object.assign({}, params);
        }

        // Save the type of event, as well as what is being logged
        message['event'] = 'log_event';
        message['type'] = logEventType;

        this.send(message);
    }
}