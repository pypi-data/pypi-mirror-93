import { ColumnarDataSource } from "models/sources/columnar_data_source";
import { ColumnDataSource } from "models/sources/column_data_source";
import * as p from "core/properties";
export declare namespace CDSCompress {
    type Attrs = p.AttrsOf<Props>;
    type Props = ColumnarDataSource.Props & {
        source: p.Property<ColumnDataSource>;
        inputData: p.Property<Record<string, any>>;
    };
}
export interface CDSCompress extends CDSCompress.Attrs {
}
export declare class CDSCompress extends ColumnarDataSource {
    properties: CDSCompress.Props;
    constructor(attrs?: Partial<CDSCompress.Attrs>);
    static __name__: string;
    static init_CDSCompress(): void;
    initialize(): void;
    inflateCompressedBokehBase64(arrayIn: any): any;
    inflateCompressedBokehObjectBase64(): any;
    view: number[] | null;
}
