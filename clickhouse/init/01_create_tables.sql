-- Создание базы данных для аналитики
CREATE DATABASE IF NOT EXISTS analytics;

-- Таблица для хранения данных о винах (справочник)
CREATE TABLE IF NOT EXISTS analytics.wines
(
    wine_id UInt32,
    name String,
    wine_type String,
    country_id UInt32,
    country_name String,
    region String,
    year UInt16,
    price Decimal(10, 2),
    volume UInt16,
    alcohol Decimal(4, 2),
    grape_variety String,
    created_at DateTime,
    updated_at DateTime DEFAULT now()
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY wine_id;

-- Таблица для аналитики продаж (факты)
CREATE TABLE IF NOT EXISTS analytics.sales
(
    sale_id UInt64,
    wine_id UInt32,
    wine_name String,
    wine_type String,
    country_name String,
    quantity UInt32,
    price Decimal(10, 2),
    total_amount Decimal(12, 2),
    sale_date DateTime,
    year UInt16,
    month UInt8,
    day UInt8,
    hour UInt8,
    day_of_week UInt8,
    created_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(sale_date)
ORDER BY (sale_date, wine_id)
TTL sale_date + INTERVAL 2 YEAR;

-- Таблица для финансовых показателей (агрегированные данные)
CREATE TABLE IF NOT EXISTS analytics.daily_metrics
(
    metric_date Date,
    total_sales Decimal(14, 2),
    total_orders UInt32,
    avg_order_value Decimal(10, 2),
    unique_wines_sold UInt32,
    top_wine_type String,
    created_at DateTime DEFAULT now()
)
ENGINE = ReplacingMergeTree(created_at)
ORDER BY metric_date;

-- Материализованное представление для ежедневной статистики
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.daily_sales_mv
ENGINE = SummingMergeTree()
ORDER BY (sale_date, wine_type)
AS SELECT
    toDate(sale_date) as sale_date,
    wine_type,
    sum(quantity) as total_quantity,
    sum(total_amount) as total_revenue,
    count() as order_count,
    avg(price) as avg_price
FROM analytics.sales
GROUP BY sale_date, wine_type;

-- Материализованное представление для статистики по странам
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.country_sales_mv
ENGINE = SummingMergeTree()
ORDER BY (sale_date, country_name)
AS SELECT
    toDate(sale_date) as sale_date,
    country_name,
    sum(quantity) as total_quantity,
    sum(total_amount) as total_revenue,
    count() as order_count
FROM analytics.sales
GROUP BY sale_date, country_name;

-- Таблица для отслеживания синхронизации
CREATE TABLE IF NOT EXISTS analytics.sync_log
(
    sync_id UInt64,
    table_name String,
    records_synced UInt32,
    sync_start DateTime,
    sync_end DateTime,
    status String,
    error_message String
)
ENGINE = MergeTree()
ORDER BY sync_start;
