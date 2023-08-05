from pxapi.vizierapipb import vizierapi_pb2 as vpb


class PxLError(Exception):
    pass


def _format_line(line_num: int, line: str, column: int, message: str) -> str:
    TAB = "  "
    if column > len(line):
        return "\n".join([line, message])
    column_pointer = len(line) * [" "]
    column_pointer[column - 1] = "^"
    out = [
        f"PxL, line {line_num}, {message}",
        line,
        "".join(column_pointer),
    ]
    return TAB + ("\n" + TAB + TAB).join(out)


def _line_col_exception(query: str, error_details: vpb.ErrorDetails, cluster_id: str) -> PxLError:
    query_lines = query.splitlines()
    combined_message = [""]

    for detail in error_details:
        if not detail.compiler_error:
            continue
        err = detail.compiler_error
        combined_message.append(_format_line(
            err.line,
            query_lines[err.line - 1],
            err.column,
            err.message
        ))

    return PxLError(f"cluster: {cluster_id}\n".join(combined_message))


def build_pxl_exception(query: str, err: vpb.Status, cluster_id: str) -> Exception:
    if not err.error_details:
        return ValueError(f"On {cluster_id} {err.message}")
    return _line_col_exception(query, err.error_details, cluster_id)
