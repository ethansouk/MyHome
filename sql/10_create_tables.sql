CREATE TABLE public.authorized_devices (
	device_id uuid NOT NULL ,
	mac_address varchar NOT NULL,
	"name" varchar NOT NULL,
	"role" varchar NOT NULL
);


CREATE TABLE public.sensors (
	sensor_id uuid NOT NULL ,
	"name" varchar NOT NULL,
	sensor_type varchar NOT NULL,
	"location" varchar NOT NULL,
	energy_uom varchar NOT NULL, -- watt or gallon
	energy_value float8 NOT NULL,
	CONSTRAINT sensors_pk PRIMARY KEY (sensor_id)
);

COMMENT ON COLUMN public.sensors.energy_uom IS 'watt or gallon';

CREATE TABLE public.state_type (
	state_type_id uuid NOT NULL ,
	"name" varchar NOT NULL,
	CONSTRAINT state_type_pk PRIMARY KEY (state_type_id)
);


CREATE TABLE public.usage_electricity (
	usage_electricity_id uuid NOT NULL ,
	dtm timestamptz NOT NULL DEFAULT (now() AT TIME ZONE 'utc'::text),
	predicted bool NOT NULL DEFAULT false,
	watts float8 NOT NULL DEFAULT 0,
	CONSTRAINT usage_electricity_pk PRIMARY KEY (usage_electricity_id)
);


CREATE TABLE public.usage_water (
	usage_water_id uuid NOT NULL ,
	dtm timestamptz NOT NULL DEFAULT (now() AT TIME ZONE 'utc'::text),
	predicted bool NOT NULL DEFAULT false,
	gallons float8 NOT NULL DEFAULT 0,
	CONSTRAINT usage_water_pk PRIMARY KEY (usage_water_id)
);


CREATE TABLE public.sensor_data (
	data_id uuid NOT NULL ,
	dtm timestamptz NOT NULL DEFAULT (now() AT TIME ZONE 'utc'::text),
	sensor_id uuid NOT NULL,
	state_type_id uuid NOT NULL,
	value varchar NULL,
	predicted bool NOT NULL DEFAULT false,
	CONSTRAINT data_fk FOREIGN KEY (sensor_id) REFERENCES public.sensors(sensor_id),
	CONSTRAINT sensor_data_fk FOREIGN KEY (state_type_id) REFERENCES public.state_type(state_type_id)
);

