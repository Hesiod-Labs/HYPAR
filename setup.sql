--
-- setup database file for HYPAR
--

-- create database and user, grant privileges to user
create database hypar_database;
create user 'username'@'localhost' identified by 'password';
grant all on hypar_database.* to 'username'@'localhost';
flush privileges;

-- select the database and create tables
use hypar_database;
-- entities
create table user(
    id int not null auto_increment primary key,
    username varchar(255) not null,
    password varchar(255) not null,
    email varchar(255) not null,
    IEX_API_key varchar(255) not null
);
create table portfolio(
    id int not null auto_increment primary key,
    name varchar(255) not null,
    manager varchar(255) not null
);
create table watchlist(
    id int not null auto_increment primary key,
    name varchar(255) not null
);
create table stock(
    id int not null auto_increment primary key,
    portfolio_id int not null,
    watchlist_id int not null,
    price_data_id int not null,
    balance_sheet_id int not null,
    book_data_id int not null,
    cash_flow_id int not null,
    company_data_id int not null,
    earnings_id int not null,
    income_statement_id int not null,
    intraday_data_id int not null,
    key_stats_id int not null,
    price_target_id int not null,
    ticker varchar(255) not null,
    owned boolean not null,
    num_shares int not null,
    start_date timestamp not null default current_timestamp,
    end_date timestamp null,
    foreign key (portfolio_id) references portfolio(id),
    foreign key (watchlist_id) references watchlist(id)
);
create table price_data(
    id int not null auto_increment primary key,
    stock_id int not null,
    date_price date not null,
    changing float not null,
    change_over_time float not null,
    change_percent float not null,
    close float not null,
    high float not null,
    low float not null,
    open float not null,
    u_close float not null,
    u_high float not null,
    u_low float not null,
    u_open float not null,
    u_volume bigint not null,
    volume bigint not null,
    foreign key (stock_id) references stock(id)
);
create table balance_sheet(
    id int not null auto_increment primary key,
    stock_id int not null,
    ticker varchar(255) not null,
    report_date date not null,
    current_cash bigint not null,
    short_term_investments bigint not null,
    receivables bigint not null,
    inventory bigint not null,
    other_current_assets bigint not null,
    current_assets bigint not null,
    long_term_investments bigint not null,
    property_plant_equipment bigint not null,
    goodwill bigint not null,
    intangible_assets bigint not null,
    other_assets bigint not null,
    total_assets bigint not null,
    accounts_payable bigint not null,
    current_long_term_debt bigint not null,
    other_current_liabilities bigint not null,
    total_current_liabilities bigint not null,
    long_term_debt bigint not null,
    other_liabilities bigint not null,
    minority_interest bigint not null,
    total_liabilities bigint not null,
    common_stock bigint not null,
    retained_earnings bigint not null,
    treasury_stock bigint not null,
    capital_surplus bigint not null,
    shareholder_equity bigint not null,
    net_tangible_assets bigint not null,
    foreign key (stock_id) references stock(id)
);
create table book_data(
    id int not null auto_increment primary key,
    stock_id int not null,
    ticker varchar(255) not null,
    company_name varchar(255) not null,
    calculation_price varchar(255) not null,
    open int,
    open_time bigint,
    close int,
    close_time bigint,
    high float not null,
    low float not null,
    latest_price int not null,
    latest_source varchar(255) not null,
    latest_time varchar(255) not null,
    latest_update bigint not null,
    latest_volume int not null,
    iex_real_time_price int,
    iex_real_time_size bigint,
    iex_last_updated bigint,
    delayed_price float not null,
    delayed_price_time bigint not null,
    extended_price float not null,
    extended_change float not null,
    extended_change_percent float not null,
    extended_price_time bigint not null,
    previous_close float not null,
    changed float not null,
    change_percent float not null,
    iex_market_percent float,
    iex_volume float,
    avg_total_volume int not null,
    iex_bid_price int,
    iex_bid_size int,
    iex_ask_price int,
    iex_ask_size bigint,
    market_cap bigint not null,
    pe_ratio float not null,
    week_52_high float not null,
    week_52_low float not null,
    ytd_change float not null,
    foreign key (stock_id) references stock(id)
);
create table cash_flow(
    id int not null auto_increment primary key,
    stock_id int not null,
    ticker varchar(255) not null,
    report_date date not null,
    net_income bigint not null,
    depreciation bigint not null,
    changes_in_receivables bigint not null,
    changes_in_inventories bigint not null,
    cash_change bigint not null,
    cash_flow bigint not null,
    capital_expenditures bigint not null,
    investments bigint not null,
    investing_activity_other bigint not null,
    total_investing_cash_flows bigint not null,
    dividends_paid bigint not null,
    net_borrowings bigint not null,
    other_financing_cash_flows bigint not null,
    cash_flow_financing bigint not null,
    exchange_rate_effect varchar(255) not null,
    foreign key (stock_id) references stock(id)
);
create table company_data(
    id int not null auto_increment primary key,
    stock_id int not null,
    ticker varchar(255) not null,
    company_name varchar(255) not null,
    exchange varchar(255) not null,
    industry varchar(255) not null,
    website varchar(255) not null,
    description text(10000) not null,
    CEO varchar(255) not null,
    security_name varchar(255) not null,
    issue_type varchar(255) not null,
    sector varchar(255) not null,
    employees int not null,
    foreign key (stock_id) references stock(id)
);
create table earnings(
    id int not null auto_increment primary key,
    stock_id int not null,
    ticker varchar(255) not null,
    actual_EPS float not null,
    consensus_EPS float not null,
    announce_time varchar(255) not null,
    number_of_estimates bigint not null,
    EPS_surprise_dollar float not null,
    EPS_report_date date not null,
    fiscal_period varchar(255) not null,
    fiscal_end_date date not null,
    year_ago float not null,
    year_ago_change_percent float not null,
    foreign key (stock_id) references stock(id)
);
create table income_statement(
    id int not null auto_increment primary key,
    stock_id int not null,
    ticker varchar(255) not null,
    report_date date not null,
    total_revenue bigint not null,
    cost_of_revenue bigint not null,
    gross_profit bigint not null,
    research_and_development bigint not null,
    selling_general_and_admin bigint not null,
    operating_expense bigint not null,
    operating_income bigint not null,
    other_income_expense_net bigint not null,
    ebit bigint not null,
    interest_income bigint not null,
    pretax_income bigint not null,
    income_tax bigint not null,
    minority_interest bigint not null,
    net_income bigint not null,
    net_income_basic bigint not null,
    foreign key (stock_id) references stock(id)
);
create table intraday_data(
    id int not null auto_increment primary key,
    stock_id int not null,
    ticker varchar(255) not null,
    low float not null,
    market_average float not null,
    market_change_over_time float not null,
    market_close float not null,
    market_high float not null,
    market_low float not null,
    market_notional float not null,
    market_number_of_trades int not null,
    market_open float not null,
    market_volume int not null,
    notional float not null,
    number_of_trades int not null,
    open float not null,
    volume int not null,
    foreign key (stock_id) references stock(id)
);
create table key_stats(
    id int not null auto_increment primary key,
    stock_id int not null,
    week_52_change float not null,
    week_52_high float not null,
    week_52_low float not null,
    market_cap bigint not null,
    employees int not null,
    day_200_moving_avg float not null,
    day_50_moving_avg float not null,
    floating bigint not null,
    avg_10_volume float not null,
    avg_30_volume float not null,
    ttm_EPS float not null,
    ttm_dividend_rate float not null,
    company_name varchar(255) not null,
    shares_outstanding bigint not null,
    max_change_percent float not null,
    year_5_change_percent float not null,
    year_2_change_percent float not null,
    year_1_change_percent float not null,
    ytd_change_percent float not null,
    month_6_change_percent float not null,
    month_3_change_percent float not null,
    month_1_change_percent float not null,
    day_30_change_percent float not null,
    day_5_change_percent float not null,
    next_dividend_date varchar(255) not null,
    divident_yield float not null,
    next_earnings_date date not null,
    ex_dividend_date date not null,
    pe_ratio float not null,
    beta float not null,
    foreign key (stock_id) references stock(id)
);
-- relations
create table user_portfolio(
    user_id int not null,
    portfolio_id int not null,
    foreign key (user_id) references user(id),
    foreign key (portfolio_id) references portfolio(id)
);
