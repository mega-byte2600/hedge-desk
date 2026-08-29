#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

typedef void (^HedgeDeskAPICompletion)(NSDictionary * _Nullable payload, NSError * _Nullable error);

@interface HedgeDeskAPI : NSObject

@property(nonatomic, copy) NSString *baseURL;

- (instancetype)initWithBaseURL:(NSString *)baseURL;
- (void)fetchPath:(NSString *)path completion:(HedgeDeskAPICompletion)completion;
- (void)fetchStatus:(HedgeDeskAPICompletion)completion;
- (void)fetchSchwabReadiness:(HedgeDeskAPICompletion)completion;
- (void)fetchDividends:(HedgeDeskAPICompletion)completion;
- (void)fetchEarnings:(HedgeDeskAPICompletion)completion;

@end

NS_ASSUME_NONNULL_END
