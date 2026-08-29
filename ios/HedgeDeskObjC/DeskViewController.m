#import "DeskViewController.h"
#import "HedgeDeskAPI.h"

@interface DeskViewController ()

@property(nonatomic, strong) HedgeDeskAPI *api;
@property(nonatomic, strong) NSArray<NSString *> *sections;
@property(nonatomic, strong) NSMutableDictionary<NSString *, NSArray<NSString *> *> *rows;

@end

@implementation DeskViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.title = @"Hedge Desk";
    self.api = [[HedgeDeskAPI alloc] initWithBaseURL:@"http://127.0.0.1:8765"];
    self.sections = @[@"Safety", @"Schwab", @"Dividend Desk", @"Earnings Desk"];
    self.rows = [@{
        @"Safety": @[@"Loading backend status..."],
        @"Schwab": @[@"Loading readiness..."],
        @"Dividend Desk": @[@"Loading dividend candidates..."],
        @"Earnings Desk": @[@"Loading earnings candidates..."]
    } mutableCopy];
    self.tableView.backgroundColor = [UIColor systemBackgroundColor];
    self.tableView.rowHeight = UITableViewAutomaticDimension;
    self.tableView.estimatedRowHeight = 56;
    self.refreshControl = [[UIRefreshControl alloc] init];
    [self.refreshControl addTarget:self action:@selector(refreshDesk) forControlEvents:UIControlEventValueChanged];
    [self refreshDesk];
}

- (void)refreshDesk {
    [self.api fetchStatus:^(NSDictionary *payload, NSError *error) {
        NSDictionary *schwab = payload[@"schwab"];
        NSString *mode = payload[@"mode"] ?: @"unknown";
        NSString *orders = [schwab[@"orders_blocked"] boolValue] ? @"orders blocked" : @"ORDER RISK";
        self.rows[@"Safety"] = @[[NSString stringWithFormat:@"%@ | paper only | %@", mode, orders]];
        [self.tableView reloadData];
        [self.refreshControl endRefreshing];
    }];

    [self.api fetchSchwabReadiness:^(NSDictionary *payload, NSError *error) {
        NSString *client = [payload[@"client_id_configured"] boolValue] ? @"client id ready" : @"client id missing";
        NSString *secret = [payload[@"client_secret_configured"] boolValue] ? @"secret ready" : @"secret missing";
        NSString *auth = [payload[@"ready_for_authorization_url"] boolValue] ? @"ready for auth" : @"not ready";
        self.rows[@"Schwab"] = @[[NSString stringWithFormat:@"%@ | %@ | %@", client, secret, auth]];
        [self.tableView reloadData];
    }];

    [self.api fetchDividends:^(NSDictionary *payload, NSError *error) {
        self.rows[@"Dividend Desk"] = [self rowsFromCandidates:payload[@"candidates"] fallback:@"No dividend candidates"];
        [self.tableView reloadData];
    }];

    [self.api fetchEarnings:^(NSDictionary *payload, NSError *error) {
        self.rows[@"Earnings Desk"] = [self rowsFromCandidates:payload[@"candidates"] fallback:@"No earnings candidates"];
        [self.tableView reloadData];
    }];
}

- (NSArray<NSString *> *)rowsFromCandidates:(NSArray *)candidates fallback:(NSString *)fallback {
    if (![candidates isKindOfClass:[NSArray class]] || candidates.count == 0) {
        return @[fallback];
    }
    NSMutableArray<NSString *> *result = [NSMutableArray array];
    for (NSDictionary *candidate in candidates) {
        if (![candidate isKindOfClass:[NSDictionary class]]) {
            continue;
        }
        NSString *symbol = candidate[@"symbol"] ?: @"?";
        NSString *action = candidate[@"paper_action"] ?: candidate[@"action"] ?: @"review";
        NSString *source = candidate[@"source"] ?: @"source pending";
        [result addObject:[NSString stringWithFormat:@"%@ | %@ | %@", symbol, action, source]];
    }
    return result.count ? result : @[fallback];
}

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    return self.sections.count;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    NSString *key = self.sections[section];
    return self.rows[key].count;
}

- (NSString *)tableView:(UITableView *)tableView titleForHeaderInSection:(NSInteger)section {
    return self.sections[section];
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:@"Cell"];
    if (!cell) {
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleSubtitle reuseIdentifier:@"Cell"];
        cell.textLabel.numberOfLines = 0;
        cell.textLabel.font = [UIFont preferredFontForTextStyle:UIFontTextStyleBody];
    }
    NSString *key = self.sections[indexPath.section];
    cell.textLabel.text = self.rows[key][indexPath.row];
    cell.selectionStyle = UITableViewCellSelectionStyleNone;
    return cell;
}

@end
