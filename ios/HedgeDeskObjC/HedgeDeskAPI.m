#import "HedgeDeskAPI.h"

@implementation HedgeDeskAPI

- (instancetype)initWithBaseURL:(NSString *)baseURL {
    self = [super init];
    if (self) {
        _baseURL = [baseURL copy];
    }
    return self;
}

- (void)fetchPath:(NSString *)path completion:(HedgeDeskAPICompletion)completion {
    NSString *urlString = [NSString stringWithFormat:@"%@%@", self.baseURL, path];
    NSURL *url = [NSURL URLWithString:urlString];
    if (!url) {
        NSError *error = [NSError errorWithDomain:@"HedgeDeskAPI" code:1 userInfo:@{NSLocalizedDescriptionKey: @"Invalid backend URL"}];
        completion(nil, error);
        return;
    }

    NSURLSessionDataTask *task = [[NSURLSession sharedSession] dataTaskWithURL:url completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        if (error) {
            dispatch_async(dispatch_get_main_queue(), ^{
                completion(nil, error);
            });
            return;
        }
        if (!data) {
            NSError *emptyError = [NSError errorWithDomain:@"HedgeDeskAPI" code:2 userInfo:@{NSLocalizedDescriptionKey: @"Empty backend response"}];
            dispatch_async(dispatch_get_main_queue(), ^{
                completion(nil, emptyError);
            });
            return;
        }

        NSError *jsonError = nil;
        id object = [NSJSONSerialization JSONObjectWithData:data options:0 error:&jsonError];
        NSDictionary *payload = [object isKindOfClass:[NSDictionary class]] ? object : nil;
        dispatch_async(dispatch_get_main_queue(), ^{
            completion(payload, jsonError);
        });
    }];
    [task resume];
}

- (void)fetchStatus:(HedgeDeskAPICompletion)completion {
    [self fetchPath:@"/api/status" completion:completion];
}

- (void)fetchSchwabReadiness:(HedgeDeskAPICompletion)completion {
    [self fetchPath:@"/api/schwab/readiness" completion:completion];
}

- (void)fetchDividends:(HedgeDeskAPICompletion)completion {
    [self fetchPath:@"/api/dividends" completion:completion];
}

- (void)fetchEarnings:(HedgeDeskAPICompletion)completion {
    [self fetchPath:@"/api/earnings" completion:completion];
}

@end
