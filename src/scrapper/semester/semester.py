import httpx


def post_single_semester(data: dict) -> None:
    response = httpx.post(
        "http://localhost:8080/api/semesters",
        json=data,
    )
    if response.status_code != 201:
        print(
            f"Failed to post semester data for {data}. Status code: {response.status_code}"
        )
    else:
        print(f"Successfully posted data for {data}.")


def post_semesters():
    for year in range(2020, 2028):
        for semester in ["FIRST", "SUMMER", "SECOND", "WINTER"]:
            data = {"year": year, "semester_": semester, "semester_status": "INACTIVE"}
            post_single_semester(data)


if __name__ == "__main__":
    post_semesters()
