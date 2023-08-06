# Copyright (C) 2020 Jacob Rembish

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# from datetime import date, timedelta

from pymedphys._imports import pandas as pd
from pymedphys._imports import streamlit as st

from pymedphys._streamlit import categories

from pymedphys._experimental.chartchecks.compare import (
    specific_patient_weekly_check_colour_results,
    weekly_check_colour_results,
)
from pymedphys._experimental.chartchecks.weekly_check_helpers import (
    compare_all_incompletes,
    plot_couch_deltas,
    plot_couch_positions,
    show_incomplete_weekly_checks,
)

CATEGORY = categories.PRE_ALPHA
TITLE = "Weekly Chart Review"


def main():
    # currdir = os.getcwd()

    incomplete_qcls = show_incomplete_weekly_checks()
    incomplete_qcls = incomplete_qcls.copy()
    incomplete_qcls = incomplete_qcls.drop_duplicates(subset=["patient_id"])
    # incomplete_qcls = incomplete_qcls.set_index("patient_id")

    all_delivered, weekly_check_results = compare_all_incompletes(incomplete_qcls)[1:]
    all_delivered = all_delivered.astype({"pat_ID": "str"})
    weekly_check_results = weekly_check_results.sort_values(["first_name"])
    weekly_check_results = weekly_check_results.reset_index(drop=True)
    weekly_check_results_stylized = weekly_check_results.style.apply(
        weekly_check_colour_results, axis=1
    )
    st.table(weekly_check_results_stylized)
    default = pd.DataFrame(["< Select a patient >"])
    patient_list = (
        weekly_check_results["patient_id"]
        + ", "
        + weekly_check_results["first_name"]
        + " "
        + weekly_check_results["last_name"]
    )
    patient_list = pd.concat([default, patient_list]).reset_index(drop=True)
    patient_select = st.selectbox("Select a patient: ", patient_list[0])

    if patient_select != "< Select a patient >":
        mrn = patient_select.split(",")[0]
        # planned, delivered, patient_results = compare_single_incomplete(mrn)
        todays_date = pd.Timestamp("today").floor("D")
        week_ago = todays_date + pd.offsets.Day(-7)
        delivered = all_delivered[all_delivered["mrn"] == mrn]
        delivered_this_week = delivered[delivered["date"] > week_ago]

        # plot the couch coordinates for each delivered beam
        # st.write(planned)
        # st.write(delivered_this_week)
        st.header(
            delivered_this_week.iloc[0]["first_name"]
            + " "
            + delivered_this_week.iloc[0]["last_name"]
        )

        delivered_this_week["rx_change"] = 0
        for field in range(0, len(delivered_this_week)):
            if delivered_this_week.iloc[field]["site_version"] != 0:
                delivered_this_week.iloc[field]["rx_change"] = 1

        delivered_this_week["site_setup_change"] = 0
        for field in range(0, len(delivered_this_week)):
            if delivered_this_week.iloc[field]["site_setup_version"] != 0:
                delivered_this_week.iloc[field]["site_setup_change"] = 1

        st.table(
            delivered_this_week[
                [
                    "date",
                    "fx",
                    "total_dose_delivered",
                    "site",
                    "field_name",
                    "was_overridden",
                    "partial_tx",
                    "new_field",
                    "rx_change",
                    "site_setup_change",
                ]
            ].style.apply(specific_patient_weekly_check_colour_results, axis=1)
        )

        # st.write(patient_results)

        # Create a checkbox to allow users to view treatment couch position history
        show_couch_positions = st.checkbox("Plot couch position history.")
        if show_couch_positions:
            st.subheader("Couch Positions")
            plot_couch_positions(delivered)
            plot_couch_deltas(delivered)
