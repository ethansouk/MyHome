-- public.usage_electricity_actual source

CREATE OR REPLACE VIEW public.usage_electricity_actual
AS SELECT ue.usage_electricity_id,
    ue.dtm,
    ue.watts
   FROM usage_electricity ue
  WHERE ue.predicted = false;


-- public.usage_electricity_predicted source

CREATE OR REPLACE VIEW public.usage_electricity_predicted
AS SELECT ue.usage_electricity_id,
    ue.dtm,
    ue.watts
   FROM usage_electricity ue
  WHERE ue.predicted = true;